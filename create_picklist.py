from db import dbtools
from tbainfo import tbarequests
from picklist_team import Team
import numpy as np
import globals


def main():
    globals.init()
    db = dbtools("Champs", "frc900", "frc900")
    tba = tbarequests('jQusM2aYtJLHXv3vxhDcPpIWzaxjMga5beNRWOarv6wdRwTF63vNpIsLYVANvCWE')

    cargo_weight = int(globals.cargo_weight)/100
    panel_weight = int(globals.panel_weight)/100
    endgame_weight = int(globals.endgame_weight)/100

    team_keys = tba.get_teams(globals.tba_competition_id)

    teams = []

    # create and populate team objects
    for team_key in team_keys:
        team = new_team(team_key, db)
        teams.append(team)

    mean_cargo = np.mean([team.cargo for team in teams])
    std_cargo = np.std([team.cargo for team in teams])
    mean_panel = np.mean([team.panel for team in teams])
    std_panel = np.std([team.panel for team in teams])

    for team in teams:
        team.cargo_zscore = float((team.cargo - mean_cargo) / std_cargo)
        team.panel_zscore = (team.panel - mean_panel) / std_panel
        team.endgame_score = compute_endgame_score(team)

    picklist = [i for i in sorted(teams, key=lambda x: (x.cargo_zscore * (cargo_weight/100) + x.panel_zscore * (panel_weight/100 + x.endgame_score * (endgame_weight/100))), reverse=True)]
    out = open('pick.txt', 'w')

    for team in picklist:
        out.write(team.get_data(picklist.index(team)))

    out.close()


def new_team(team_key, db):
    team_id = db.get_team_id(team_key)
    comp_id = db.get_competition_id(globals.competition)
    matches_team_ids = db.get_matches_team_id(team_id, comp_id, globals.match_cutoff)
    team = Team(team_key, team_id)

    team.matches = matches_team_ids
    team.cargo = np.mean(db.get_metric(matches_team_ids, "'Cargo'", ''))
    team.panel = np.mean(db.get_metric(matches_team_ids, "'Panel'", ''))
    team.cargo_raw = db.get_metric(matches_team_ids, "'Cargo'", '')
    team.panel_raw = db.get_metric(matches_team_ids, "'Panel'", '')
    team.endgame = db.get_status(matches_team_ids, 'endgame')
    team.auto = db.get_status(matches_team_ids, 'auto')
    team.L3 = team.endgame.count('Level 3')
    team.L2 = team.endgame.count('Level 2')
    team.L1 = team.endgame.count('Level 1')

    return team


def compute_endgame_score(team):
    score = 0
    score += team.L1 * 1 + team.L2 * 2 + team.L3 * 4
    score = score/len(team.endgame)

    return score


main()
