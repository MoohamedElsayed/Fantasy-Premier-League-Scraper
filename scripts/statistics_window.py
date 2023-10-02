from PyQt5 import QtCore , QtGui, QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, QSortFilterProxyModel , pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import  QVBoxLayout, QWidget, QTableView, QLineEdit, QHBoxLayout, QLabel,QComboBox
import sys
import mysql.connector


class TableModel(QAbstractTableModel):
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

    closed = pyqtSignal()

    def __init__(self):
        super(StatisticsWindow, self).__init__()
        self.table = QTableView()

        # Fetching the data for the database
        self.data, self.colnames = self.fetch_data_from_database(user = 'mohamed')

        # Creating table model with the data
        self.model = TableModel(self.data, self.colnames)
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



    def fetch_data_from_database(self, host = 'localhost', user = 'root', password = 'password', dbname = 'fpl'):
        """
        Parameters:
            host (str) (optional) : name of the host, default is 'localhost'.
            user (str) (optional) : name of the user, default is 'root'.
            password (optional) : user password, default is 'password'.
            dbname (optional) : name of the database to be created , default is 'fpl'.


        Returns:
            Result : All the data in the database
            Column names : The column names of the data returned

        """
                           # Creating a connection to the database.
        conn = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = dbname
        )
        cur = conn.cursor()

        # Defining the sql Syntax.
        sql =   """
                SELECT CONCAT(p.first_name, ' ', p.second_name) AS Name,
                       t.name AS 'Team Name', 
                       po.position_name AS 'Position',
                       p.cost / 10.0 AS Cost,
                       pp.total_points AS 'Total Points', 
                       pp.form AS Form, 
                       pp.goals_scored AS 'Goals Scored',
                       pp.bonus_points AS 'Bonus Points', 
                       pp.points_per_game AS 'Points Per Game', 
                       pp.selected_by_percent AS 'Selected By Percent', 
                       pp.minutes_played AS 'Minutes Played', 
                       pp.threat AS Threat,
                       pp.assists AS Assists, 
                       pp.clean_sheets AS 'Clean Sheets',
                       pp.goals_conceded AS 'Goals Conceded', 
                       pp.yellow_cards AS 'Yellow Cards', 
                       pp.red_cards AS 'Red Cards',
                       pp.games_started AS 'Games Started', 
                       t.strength AS 'Team Strength'
                  FROM team AS t
                  JOIN player AS p ON t.id = p.team_id
                  JOIN player_performance AS pp ON p.id = pp.player_id
                  JOIN position AS po ON po.id = p.position_id
                 ORDER BY 5 DESC
                """
        cur.execute(sql)

        # Fetching the data and columns names
        result = cur.fetchall()
        col_names = cur.column_names
        
        # Closing the connection and returning the data
        cur.close()
        conn.close()

        return result, col_names
    
    def closeEvent(self, event):
        self.closed.emit()
        event.accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StatisticsWindow()
    win.show()
    sys.exit(app.exec_())
