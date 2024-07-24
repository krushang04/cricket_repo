from flask import render_template, request, jsonify
from app import app
from app.data_processor import load_match_data

MATCH_DATA = load_match_data(app.config['JSON_FILE_PATH'])

def calculate_run_rate(runs, overs):
    return runs / overs if overs > 0 else 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estimate', methods=['POST'])
def estimate():
    data = request.json
    team_a = data['team_a']
    team_b = data['team_b']
    batting_first = data['batting_first']
    runs_scored = int(data['runs_scored'])
    wickets_fallen = int(data['wickets_fallen'])
    overs_completed = float(data['overs_completed'])
    runs_required = int(data['runs_required'])

    current_run_rate = calculate_run_rate(runs_scored, overs_completed)
    required_run_rate = calculate_run_rate(runs_required, 20 - overs_completed)

    factors = {
        'runs_comparison': 0,
        'wickets_in_hand': 0,
        'run_rate_comparison': 0,
        'required_run_rate': 0
    }

    if batting_first == MATCH_DATA['innings_1_team']:
        runs_diff = runs_scored - MATCH_DATA['innings_1_score'] * (overs_completed / 20)
    else:
        runs_diff = (runs_scored / overs_completed) - (MATCH_DATA['innings_2_score'] / 20)
    factors['runs_comparison'] = min(max(runs_diff / 10, -1), 1)

    factors['wickets_in_hand'] = (10 - wickets_fallen) / 10

    if batting_first == MATCH_DATA['innings_1_team']:
        rr_diff = current_run_rate - calculate_run_rate(MATCH_DATA['innings_1_score'], MATCH_DATA['innings_1_overs'])
    else:
        rr_diff = current_run_rate - calculate_run_rate(MATCH_DATA['innings_2_score'], MATCH_DATA['innings_2_overs'])
    factors['run_rate_comparison'] = min(max(rr_diff, -1), 1)

    if not batting_first:
        factors['required_run_rate'] = min((10 - required_run_rate) / 5, 1)

    weights = {
        'runs_comparison': 0.3,
        'wickets_in_hand': 0.3,
        'run_rate_comparison': 0.2,
        'required_run_rate': 0.2
    }
    probability = sum(factor * weights[key] for key, factor in factors.items() if key in weights)
    probability = max(min(probability + 0.5, 1), 0)

    scenario = {
        'team_a': MATCH_DATA['team_a'],
        'team_b': MATCH_DATA['team_b'],
        'batting_first': MATCH_DATA['innings_1_team'],
        'runs_scored': MATCH_DATA['innings_1_score'],
        'wickets_fallen': MATCH_DATA['innings_1_wickets'],
        'overs_completed': MATCH_DATA['innings_1_overs'],
        'runs_required': MATCH_DATA['innings_2_score'] + 1,
        'winning_team': MATCH_DATA['winner']
    }

    return jsonify({
        'probability': probability,
        'scenarios': [scenario],
        'factors': factors
    })