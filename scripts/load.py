import os, os.path
import mysql.connector

def _create_mysqldb(host ,user, password ,dbname ):
    """ Creates a MYSQL Database (if not exists).
        Drops (player, team, position, player_performance) tables if they exist,
        then creates them again with the desired schema.


        Parameters:
            host (str) : name of the host.
            user (str) : name of the user.
            password : user password.
            dbname : name of the database to be created.

                    
        Returns:
            None 
    """
    # Opening a connection to MYSQL 
    conn = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        autocommit=True
    )
    cur = conn.cursor()

    # Creating The database and using it in the connection
    cur.execute(f'CREATE DATABASE IF NOT EXISTS {dbname}')
    conn.database = dbname

    # Creating the tables in database using the schema stored in .sql file
    with open(os.path.join(os.path.dirname(__file__),'FPL_DB.sql'),'r') as f:
        cur.execute(f.read(), multi=True)

    # Closing the cursor and the connection
    cur.close()
    conn.close()




def save_to_mysqldb(data, host = 'localhost', user = 'root', password = 'password', dbname = 'fpl'):
    """ Creates a MYSQL Database and save the Extracted data into it.


        Parameters:
            data (dictionary) : the data to be saved.
                    keys : players, teams, positions, playersperformance.
                    values : list of dictionaries where each dictionary is a data item.
            host (str) (optional) : name of the host, default is 'localhost'.
            user (str) (optional) : name of the user, default is 'root'.
            password (optional) : user password, default is 'password'.
            dbname (optional) : name of the database to be created , default is 'fpl'.


        Returns:
            None 
    """

    # Creating the database
    _create_mysqldb(host ,user, password ,dbname )

    # Opening a connection to the Database
    conn = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = dbname,
        autocommit=True
    )
    cur = conn.cursor()

    # Seperating data items
    teams = data['teams']
    positions = data['positions']
    players = data['players']
    playersperformance = data['playersperformance']

    # Inserting into team table 
    for team in teams:

        # Define insert statement
        cur.execute(""" insert into team(
        id,
        name,
        strength
        ) values (
        %s,
        %s,
        %s
        )""", (
        int(team["id"]),
        team["name"],
        int(team["strength"])
        ))


    # Inserting into position table 
    for position in positions:

        # Define insert statement
        cur.execute(""" insert into `position`(
        id,
        position_name,
        position_count
        ) values (
        %s,
        %s,
        %s                
        )""", (
        position["id"],
        position["position_name"],
        position["position_count"]
        ))



    # Inserting into player table 
    for player in players:

        # Define insert statement
        cur.execute(""" insert into player(
        id,
        team_id,
        first_name,
        second_name,
        position_id,
        cost
        ) values (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s                  
        )""", (
        int(player["id"]),
        int(player["team_id"]),
        player["first_name"],
        player["second_name"],
        int(player["position_id"]),
        int(player["cost"])
        ))


    # Inserting into player_performance table 
    for playerperformance in playersperformance:

        # Define insert statement
        cur.execute(""" insert into player_performance(
        player_id,
        form,
        total_points,
        bonus_points,
        points_per_game,
        selected_by_percent,
        threat,
        minutes_played,
        goals_scored,
        assists,
        clean_sheets,
        goals_conceded,
        yellow_cards,
        red_cards,
        games_started
        ) values (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s                
        )""", (
        playerperformance["player_id"],
        float(playerperformance["form"]),
        playerperformance["total_points"],
        playerperformance["bonus_points"],
        float(playerperformance["points_per_game"]),
        float(playerperformance["selected_by_percent"]), 
        float(playerperformance["threat"]),
        playerperformance["minutes_played"], 
        playerperformance["goals_scored"],
        playerperformance["assists"], 
        playerperformance["clean_sheets"],
        playerperformance["goals_conceded"],
        playerperformance["yellow_cards"],
        playerperformance["red_cards"], 
        playerperformance["games_started"]
        ))

    # Closing the connection
    conn.close()



def _safe_open_w(path):
    """ Open "path" for writing, creating any parent directories as needed.

        Parameters: 
            path (str) : The path to the file which will be opened

        Returns:
            The file opened in write mode
    """

    # Making the file and the path if they don't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    return open(path, 'w')



def save_to_csv(data):
    """ Saving the data into csv file in folder named 'fpl_data' 

        Parameters:
            data (dictionary) : the data to be saved.
                    keys : players, teams, positions, playersperformance.
                    values : list of dictionaries where each dictionary is a data item.
        Returns:
            None
    """

    # Iterating over the dictionary keys, values and writing them into seperate csv files
    for key, value in data.items():

        with _safe_open_w(os.getcwd() + f'/fpl_data/{key}.csv') as f:

            # writing headers
            f.write(','.join(value[0].keys()))
            f.write('\n')

            #writing data
            for row in value:
                f.write(','.join(str(x) for x in row.values()))
                f.write('\n')
