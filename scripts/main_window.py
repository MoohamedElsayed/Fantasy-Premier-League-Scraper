from PyQt5 import QtCore , QtGui, QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, QSortFilterProxyModel , pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QDialogButtonBox, QFormLayout
from PyQt5.QtWidgets import  QVBoxLayout, QWidget, QTableView, QLineEdit, QHBoxLayout, QLabel,QComboBox, QPushButton,QMessageBox
import sys
import mysql.connector
from extract import extract
from load import save_to_csv, save_to_mysqldb
from statistics_window import StatisticsWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Welcome to Fantasy Premier Leauge Scraper')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("fpl_logo.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.setFixedSize(400,300)

        self.extracted_data = None

        self.scrape_button = QPushButton('Fetch FPL Data')
        self.scrape_button.clicked.connect(self.scrape_data)

        self.savecsv_button = QPushButton('Save Data to CSV Files')
        self.savecsv_button.clicked.connect(self.save_tocsv)

        self.savedb_button = QPushButton('Save Data to MYSQL DataBase')
        self.savedb_button.clicked.connect(self.save_todb)

        self.showstatistics_button = QPushButton('Show Players Statistics')
        self.showstatistics_button.clicked.connect(self.show_statictics)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.scrape_button)
        self.layout.addWidget(self.savecsv_button)
        self.layout.addWidget(self.savedb_button)
        self.layout.addWidget(self.showstatistics_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        
    def scrape_data(self):

        try:
            self.extracted_data = extract()
            msg = QMessageBox()
            msg.setWindowTitle('Fetch Data')
            msg.setText('Data Fetched Succesfully.')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        except:
            msg = QMessageBox()
            msg.setWindowTitle('Fetch Data')
            msg.setText("Couldn't Fetch Data.\nCheck your internet Connection.")
            msg.setStandardButtons(QMessageBox.Abort)
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    def save_tocsv(self):
        if self.extracted_data:
            self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
            if self.folderpath == '' : return
            try:
                print(self.folderpath)
                save_to_csv(self.extracted_data, self.folderpath)
                msg = QMessageBox()
                msg.setWindowTitle('Save to CSV')
                msg.setText('Data Saved to CSV Files Succesfully.')
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
            except:
                msg = QMessageBox()
                msg.setWindowTitle('Save to CSV')
                msg.setText("Couldn't Save Data To CSV Files.")
                msg.setStandardButtons(QMessageBox.Abort)
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Save to MYSQL DataBase')
            msg.setText("You didn't Extract the data yet !")
            msg.setStandardButtons(QMessageBox.Abort)
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    def save_todb(self):
        if self.extracted_data:
            self.input_dialog = DBInputWindow()
            self.input_dialog.exec()
            if self.input_dialog.ok_pressed:
                self.localhost, self.user, self.password = self.input_dialog.getInputs()
                if self.localhost == '' : self.localhost = 'localhost'
                if self.user == '' : self.user = 'user'
                if self.password == '' : self.password = 'password'

                try: 
                    save_to_mysqldb(self.extracted_data, host = self.localhost , user = self.user, password = self.password)
                    msg = QMessageBox()
                    msg.setWindowTitle('Save to MYSQL DataBase')
                    msg.setText('Data Saved to MYSQL DataBase Succesfully.')
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle('Save to MYSQL DataBase')
                    msg.setText("Couldn't Save Data To MYSQL DataBase.\n- Make sure that the database login information are right.")
                    msg.setStandardButtons(QMessageBox.Abort)
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Save to MYSQL DataBase')
            msg.setText("You didn't Extract the data yet !")
            msg.setStandardButtons(QMessageBox.Abort)
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    def show_statictics(self):
        self.stat_window = StatisticsWindow()
        self.stat_window.closed.connect(self.show)
        self.stat_window.show()
        self.hide()


class DBInputWindow(QDialog):
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

        layout = QFormLayout(self)
        layout.addWidget(QLabel("Leave Null For default Values."))
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




if __name__ =='__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
