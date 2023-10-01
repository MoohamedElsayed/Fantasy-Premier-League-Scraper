from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDesktopWidget
import sys
import mysql.connector

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()


    def initUI(self):
        # Setting the size and name of our window.
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Fantasy Premier League Statistics")

        # Display the window in the center of the screen.
        win = self.frameGeometry()
        pos = QDesktopWidget().availableGeometry().center()
        win.moveCenter(pos)
        self.move(win.topLeft())

        # Fetching the data.
        data, col_names = self._fetch_data_from_database()

        # Initializing the table widget.
        self.table = QTableWidget()

        # Setting the columns count and names.
        self.table.setColumnCount(19)
        self.table.setHorizontalHeaderLabels(col_names)

        # Filling the columns with the data.
        for row_number, row_data in enumerate(data):
            self.table.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.setItem(row_number, column_number, item)

        # Set the table fields to expand to fill the contents.
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        # Add the table to the central widget.
        self.setCentralWidget(self.table)
    


    def _fetch_data_from_database(self):
        
        # Creating a connection to the database.
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'mohamed',
            password = 'password',
            database = 'fpl'
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
                       pp.points_per_game AS 'points per game', 
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


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()