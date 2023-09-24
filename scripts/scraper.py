import requests
import os, os.path
def main():

    extracted_data = extract()
    save_to_csv(extracted_data)



def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')



def save_to_csv(data):

    for key, value in data.items():

        with safe_open_w(f'/home/mohamed/Desktop/fpl/fpl_data/{key}.csv') as f:

            # writing headers
            f.write(','.join(value[0].keys()))
            f.write('\n')

            for row in value:
                f.write(','.join(str(x) for x in row.values()))
                f.write('\n')



def extract():

    url = 'https://fantasy.premierleague.com/api/bootstrap-static/' 


    r = requests.get(url)

    if r.status_code != 200:
        raise KeyError('Status Code is not 200!')
    
    data = r.json()


    players_data = data['elements']
    teams_data = data['teams']
    positions_data = data['element_types']


    players = []
    playersperformance= []
    teams = []
    positions = []


    for player in players_data:

        player_item = {}
        playerperformance_item = {}

        # adding player data 
        player_item['id'] = player['id']
        player_item['first_name']  = player['first_name']
        player_item['second_name']  = player['second_name']  
        player_item['team_id'] = player['team']
        player_item['position_id']  = player['element_type']
        player_item['cost']  = player['now_cost']

        # adding player performence data
        playerperformance_item['player_id']  = player['id']
        playerperformance_item['form']  = player['form']
        playerperformance_item['total_points']  = player['total_points']
        playerperformance_item['bonus_points']  = player['bonus']
        playerperformance_item['points_per_game']  = player['points_per_game']
        playerperformance_item['selected_by_percent']  = player['selected_by_percent']
        playerperformance_item['threat']  = player['threat']
        playerperformance_item['minutes_played']  = player['minutes']
        playerperformance_item['goals_scored']  = player['goals_scored']
        playerperformance_item['assists']  = player['assists']
        playerperformance_item['clean_sheets']  = player['clean_sheets']
        playerperformance_item['goals_conceded']  = player['goals_conceded']
        playerperformance_item['yellow_cards']  = player['yellow_cards']
        playerperformance_item['red_cards']  = player['red_cards']
        playerperformance_item['games_started']  = player['starts']


        players.append(player_item)
        playersperformance.append(playerperformance_item)



    for team in teams_data:

        team_item = {}

        # adding team data
        team_item['id']  = team['id']
        team_item['name']  = team['name']
        team_item['strength']  = team['strength']

        teams.append(team_item)


    for position in positions_data:

        position_item = {}

        # adding position data 
        position_item['id']  = position['id']
        position_item['position_name']  = position['singular_name']
        position_item['position_count']  = position['element_count']

        positions.append(position_item)

    return {'players':players, 'teams':teams, 'positions':positions, 'playersperformance':playersperformance}

    

if __name__ == "__main__":
    main()