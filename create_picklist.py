from db import dbtools
from tbainfo import tbarequests
import json
from team import Team
import numpy as np


def main():
    db = dbtools("2019Scouting", "frc900", "frc900")
    tba = tbarequests('jQusM2aYtJLHXv3vxhDcPpIWzaxjMga5beNRWOarv6wdRwTF63vNpIsLYVANvCWE')
    with open('picklist_params.json') as f:
        data = json.load(f)

    cargo_weight = int(data["cargo_weight"])/100
    panel_weight = int(data["panel_weight"])/100
    endgame_weight = int(data["endgame_weight"])/100

    team_keys = tba.get_teams(data["tba_competitionid"])

    teams = []

    for team_key in team_keys:
        team = new_team(team_key, db, data)
        teams.append(team)

    mean_cargo = np.mean([team.cargo for team in teams])
    std_cargo = np.std([team.cargo for team in teams])
    mean_panel = np.mean([team.panel for team in teams])
    std_panel = np.std([team.panel for team in teams])

    for team in teams:
        team.cargo_zscore = float((team.cargo - mean_cargo) / std_cargo)
        team.panel_zscore = (team.panel - mean_panel) / std_panel

    print([i.tba_id for i in sorted(teams, key=lambda x: (x.cargo_zscore * (int(data['cargo_weight'])/100) + x.panel_zscore * (int(data['panel_weight']))/100), reverse=True)])

def new_team(team_key, db, data):
    team_id = db.get_team_id(team_key)
    comp_id = db.get_competition_id(data["competition"])
    matches_team_ids = db.get_matches_team_id(team_id, comp_id, int(data["match_cutoff"]))
    team = Team(team_key, team_id)

    team.cargo = np.mean(db.get_metric(matches_team_ids, "'Cargo'"))
    team.panel = np.mean(db.get_metric(matches_team_ids, "'Panel'"))
    team.endgame = db.get_auto_metric(matches_team_ids, 'endgame')
    team.L3 = team.endgame.count('Level 3')
    team.L2 = team.endgame.count('Level 2')
    team.L1 = team.endgame.count('Level 1')

    return team


main()