from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import  QWidget,QComboBox, QPushButton,QMessageBox,QApplication, QMainWindow, QFormLayout


from statistics_window import StatisticsWindow, DBInputWindow, MassageWindow
from extract import extract
from load import save_to_csv, save_to_mysqldb

import pandas as pd
import sys
import mysql.connector

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.data, self.colnames = None, None
        self.setWindowTitle('Welcome to Fantasy Premier Leauge Scraper')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("fpl_logo.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.setFixedSize(400,175)
        

        self.extracted_data = None

        self.scrape_button = QPushButton('Fetch FPL Data')
        self.scrape_button.clicked.connect(self.scrape_data)

        self.savecsv_button = QPushButton('Save Data to CSV Files')
        self.savecsv_button.clicked.connect(self.save_tocsv)

        self.savedb_button = QPushButton('Save Data to MYSQL DataBase')
        self.savedb_button.clicked.connect(self.save_todb)


        self.showstatistics_button = QPushButton('Show Players Statistics')
        self.showstatistics_button.clicked.connect(self.show_statictics)

        self.show_option = 0
        self.show_options = QComboBox()
        self.show_options.addItems(['Data Fetched', 'Data in the Database'])
        self.show_options.currentIndexChanged.connect(self.show_option_changed)

        self.layout = QFormLayout()

        self.layout.addRow(self.scrape_button)
        self.layout.addRow(self.savecsv_button)
        self.layout.addRow(self.savedb_button)
        self.layout.addRow('Select Where to show data from : ',self.show_options)
        self.layout.addRow(self.showstatistics_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        
    def scrape_data(self):

        try:
            self.extracted_data = extract()
            msg = MassageWindow(title='Fetch Data',
                                text='Data Fetched Succesfully.',
                                button = 'Ok',
                                icon='Information')
            msg.exec_()
        except :
            msg = MassageWindow(title = 'Fetch Data',
                                text="Couldn't Fetch Data.\nCheck your internet Connection.",
                                button = 'Abort',
                                icon='Critical')
            msg.exec_()

    def save_tocsv(self):
        if self.extracted_data:
            self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
            if self.folderpath == '' : return
            try:
                save_to_csv(self.extracted_data, self.folderpath)
                msg = MassageWindow(title='Save to CSV',
                                    text='Data Saved to CSV Files Succesfully.',
                                    button = 'Ok',
                                    icon='Information')
                msg.exec_()
            except:
                msg = MassageWindow(title = 'Save to CSV',
                                    text="Couldn't Save Data To CSV Files.",
                                    button = 'Abort',
                                    icon='Critical')
                msg.exec_()

        else:
            msg = MassageWindow(title = 'Save to MYSQL DataBase',
                                text="You didn't Fetch the data yet !",
                                button = 'Abort',
                                icon='Critical')
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
                    msg = MassageWindow(title='Save to MYSQL DataBase',
                                        text='Data Saved to MYSQL DataBase Succesfully.',
                                        button = 'Ok',
                                        icon='Information')
                    msg.exec_()

                except:
                    msg = MassageWindow(title = 'Save to MYSQL DataBase',
                                        text="Couldn't Save Data To MYSQL DataBase.\n- Make sure that the database login information are right.",
                                        button = 'Abort',
                                        icon='Critical')
                    msg.exec_()
        else:
            msg = MassageWindow(title = 'Save to MYSQL DataBase',
                                text="You didn't Extract the data yet !",
                                button = 'Abort',
                                icon='Critical')
            msg.exec_()

    def show_statictics(self):
        if self.show_option == 1:
            self.input_dialog = DBInputWindow()
            self.input_dialog.exec()
            if self.input_dialog.ok_pressed:
                self.localhost, self.user, self.password = self.input_dialog.getInputs()
                if self.localhost == '' : self.localhost = 'localhost'
                if self.user == '' : self.user = 'user'
                if self.password == '' : self.password = 'password'
            # Fetching the data for the database
            try :
                self.data, self.colnames = self.fetch_data_from_database(host = self.localhost, user = self.user, password=self.password)
                self.stat_window = StatisticsWindow(self.data, self.colnames)
                self.data, self.colnames = None, None
                self.stat_window.closed.connect(self.show)
                self.stat_window.show()
                self.hide()
                   
            except:
                msg = QMessageBox()
                msg.setWindowTitle('Show Statistics from Data in DataBase')
                msg.setText("Couldn't Fetch Data From MYSQL DataBase.\n- Make sure that the database login information are right.")
                msg.setStandardButtons(QMessageBox.Abort)
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
        elif self.show_option == 0:

            try :
                self.colnames = ['Name','Team Name', 'Position', 'Cost', 'Total Points','Form','Goals Scored','Bonus Points',
                                'Points Per Game','Selected By Percent','Minutes Played','Threat' , 'Assists',
                                'Clean Sheets','Goals Conceded', 'Yellow Cards','Red Cards','Games Started','Team Strength']
                
                players = pd.DataFrame(self.extracted_data['players'])
                players.rename(columns={'id':'player_id'}, inplace=True)
                teams = pd.DataFrame(self.extracted_data['teams'])
                teams.rename(columns={'id':'team_id'}, inplace=True)
                positions =  pd.DataFrame(self.extracted_data['positions'])
                positions.rename(columns={'id':'position_id'}, inplace=True)
                playersperformance = pd.DataFrame(self.extracted_data['playersperformance'])

                merged = pd.merge(players,teams,on=['team_id'])
                merged = pd.merge(merged,positions,on=['position_id'])
                merged = pd.merge(merged,playersperformance,on=['player_id'])
                merged = merged.to_dict(orient='records')


                self.data = []
                for player in merged:
                    self.data.append((
                        player['first_name'] + ' ' + player['second_name'],
                        player['name'],
                        player['position_name'],
                        player['cost']/10.0,
                        player['total_points'],
                        float(player['form']),
                        player['goals_scored'],
                        player['bonus_points'],
                        float(player['points_per_game']),
                        float(player['selected_by_percent']),
                        player['minutes_played'],
                        float(player['threat']),
                        player['assists'],
                        player['clean_sheets'],
                        player['goals_conceded'],
                        player['yellow_cards'],
                        player['red_cards'],
                        player['games_started'],
                        player['strength']
                    ))
                self.stat_window = StatisticsWindow(self.data, self.colnames)
                self.data, self.colnames = None, None
                self.stat_window.closed.connect(self.show)
                self.stat_window.show()
                self.hide()
                   
            except:
                msg=MassageWindow(title = 'Show Statistics from Fetched data.',
                                  text="You didn't Fetch the data yet !",
                                  icon = 'Critical',
                                  button = 'Abort')
                msg.exec_()

            
    def show_option_changed(self, index):
        self.show_option = index


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
    




if __name__ =='__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
