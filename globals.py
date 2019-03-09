import json


def init():
    with open('params.json') as f:
        data = json.load(f)

    global competition
    global tba_competition_id
    global match_cutoff
    global cargo_weight
    global panel_weight
    global endgame_weight

    competition = data['competition']
    tba_competition_id = data['tba_competitionid']
    match_cutoff = data['match_cutoff']
    cargo_weight = data['cargo_weight']
    panel_weight = data['panel_weight']
    endgame_weight = data['endgame_weight']