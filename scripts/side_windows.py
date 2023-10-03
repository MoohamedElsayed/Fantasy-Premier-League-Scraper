from PyQt5 import QtCore , QtGui, QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, QSortFilterProxyModel , pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QDialog, QFormLayout, QDialogButtonBox, QMessageBox
from PyQt5.QtWidgets import  QVBoxLayout, QWidget, QTableView, QLineEdit, QHBoxLayout, QLabel,QComboBox

class TableModel(QAbstractTableModel):
    """Table model class to create our the data table with"""
    def __init__(self, data, colnames):
        super().__init__()
        self._data = data
        self._colnames = colnames

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])
    
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        # Attaching headers to the table
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._colnames[section]
        
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return self._data[section][0]
                
        
        return super().headerData(section, orientation, role)


class StatisticsWindow(QMainWindow):
    """Window to show statistics data for the player """

    closed = pyqtSignal()

    def __init__(self, data, colnames):
        super(StatisticsWindow, self).__init__()
        self.table = QTableView()
        self._data, self._colnames = data, colnames


        # Creating table model with the data
        self.model = TableModel(self._data, self._colnames)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(0)
        self.proxy_model.setFilterCaseSensitivity(False)
        self.proxy_model.setSourceModel(self.model)
        
        # Sorting the values with Total points (default) and allow the user to sort by any column
        self.proxy_model.sort(4, Qt.DescendingOrder)
        self.table.setSortingEnabled(True)

        # Filling the table with data and resizing the columns to contents
        self.table.setModel(self.proxy_model)
        self.table.horizontalHeader().setSectionResizeMode( QtWidgets.QHeaderView.Fixed)
        self.table.verticalHeader().setSectionResizeMode( QtWidgets.QHeaderView.Fixed)
        self.table.horizontalHeader().setFont(QtGui.QFont("Arial", 12,100))
        self.table.setFont(QtGui.QFont("Arial", 12))
        self.table.resizeColumnsToContents()
        self.table.hideColumn(0)

        # Creating search layout to allow user to search for diffrent columns
        search_layout  = QHBoxLayout()

        self.searchbar = QLineEdit()
        self.searchbar.setFont(QtGui.QFont("Arial", 12))
        self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)

        search = QLabel('Search By : ')
        search.setFont(QtGui.QFont("Arial", 12,100))

        select_col = QComboBox()
        select_col.addItems(['Name', 'Team', 'Position'])
        select_col.setFont(QtGui.QFont("Arial", 12,100))
        select_col.currentIndexChanged.connect(self.filtered_col_changed)

        search_layout.addWidget(search)
        search_layout.addWidget(select_col)
        search_layout.addWidget(self.searchbar)

        # Creating the final layout and adding it to the window
        layout = QVBoxLayout()

        layout.addLayout(search_layout)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.showMaximized()

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("fpl_logo.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.setWindowTitle('Fantasy Premier Leauge Statistics')


    # Function to change the column to be filtered on 
    def filtered_col_changed(self, index):
        self.proxy_model.setFilterKeyColumn(index)



    # handler for signal when closing the window
    def closeEvent(self, event):
        self.closed.emit()
        event.accept()


class DBInputWindow(QDialog):
    """Window to Take input (host, user, password) from user"""
    ok_pressed = 0
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('DataBase Information')
        self.setFixedSize(400,150)

        self.localhost = QLineEdit(self)
        self.localhost.setPlaceholderText('default : localhost')

        self.user = QLineEdit(self)
        self.user.setPlaceholderText('default : user')

        self.password = QLineEdit(self)
        self.password.setPlaceholderText('default : password')

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        self.informative_text = QLabel("Leave Null For default Values.")
        self.informative_text.setFont(QtGui.QFont("Arial", 10,50))

        layout = QFormLayout(self)
        layout.addWidget(self.informative_text)
        layout.addRow("Enter localhost", self.localhost)
        layout.addRow("Enter user name", self.user)
        layout.addRow("Enter user password", self.password)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def accept(self) -> None:
        self.ok_pressed = 1
        return super().accept()
    
    def getInputs(self):
        return self.localhost.text(), self.user.text(), self.password.text()



class MassageWindow(QMessageBox):
    """Window ro show message to the user"""
    def __init__(self, title,text,button,icon):
        super(MassageWindow, self).__init__()
        self.setWindowTitle(title)
        self.setText(text)
        if button == 'Abort':
            self.setStandardButtons(QMessageBox.Abort)
        elif button =='Ok':
            self.setStandardButtons(QMessageBox.Ok)
        
        if icon == 'Critical':
            self.setIcon(QMessageBox.Critical)
        elif icon == 'Information':
            self.setIcon(QMessageBox.Information)

        self.setFont(QtGui.QFont("Arial", 12))

