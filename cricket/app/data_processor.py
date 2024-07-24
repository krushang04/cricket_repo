import json
from datetime import datetime

def load_match_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    innings_1 = data['innings'][0]
    innings_2 = data['innings'][1]
    
    processed_data = {
        'match_date': datetime.strptime(data['info']['dates'][0], '%Y-%m-%d').date(),
        'venue': data['info']['venue'],
        'team_a': data['info']['teams'][0],
        'team_b': data['info']['teams'][1],
        'toss_winner': data['info']['toss']['winner'],
        'toss_decision': data['info']['toss']['decision'],
        'innings_1_team': innings_1['team'],
        'innings_1_score': sum(delivery['runs']['total'] for over in innings_1['overs'] for delivery in over['deliveries']),
        'innings_1_wickets': sum(1 for over in innings_1['overs'] for delivery in over['deliveries'] if 'wicket' in delivery),
        'innings_1_overs': len(innings_1['overs']),
        'innings_2_team': innings_2['team'],
        'innings_2_score': sum(delivery['runs']['total'] for over in innings_2['overs'] for delivery in over['deliveries']),
        'innings_2_wickets': sum(1 for over in innings_2['overs'] for delivery in over['deliveries'] if 'wicket' in delivery),
        'innings_2_overs': len(innings_2['overs']),
        'winner': data['info']['outcome']['winner'],
        'win_type': list(data['info']['outcome']['by'].keys())[0],
        'win_margin': list(data['info']['outcome']['by'].values())[0]
    }
    
    return processed_data