import numpy as np
from scipy.stats import truncnorm
from db import dbtools
import tbainfo

CARGO_PT = 3
PANEL_PT = 2
AUTO1 = 3
AUTO2 = 6
CLIMB1 = 3
CLIMB2 = 6
CLIMB3 = 12


def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


def get_predicted_mean(data):
    mu, sigma, max, min = np.mean(data), np.std(data), float(np.max(data)), float(np.min(data))
    s = get_truncated_normal(mu, sigma, min, max).rvs(1000)
    mean = np.mean(s)
    return mean


def run_sim(match_number):
    db = dbtools("2018Scouting", "frc900", "frc900")
    competition_id = db.getCompetitionId("'competition'")
    alliances = tbainfo.get_match_teams(match_number)
    points = 0

    for alliance in alliances:

        for team in alliance:

            team_id = db.get_team_id(team)
            matches_team_ids = db.get_matches_team_id(team_id, competition_id)

            cargo = get_predicted_mean(db.get_metric(matches_team_ids, 'Cargo'))
            panel = get_predicted_mean(db.get_metric(matches_team_ids, 'Panel'))

            auto_vals = db.get_metric(matches_team_ids, 'cross_auto_line')
            auto = []
            for i in auto_vals:
                if i == 'level_2':
                    auto.append(AUTO2)
                else:
                    auto.append(AUTO1)

            climb = []
            climb_vals = db.get_metric(matches_team_ids, 'endgame_status')
            for i in climb_vals:
                if i == 'level_3':
                    auto.append(CLIMB3)
                elif i == 'level 2':
                    auto.append(CLIMB2)
                else:
                    auto.append(CLIMB1)

        points = (CARGO_PT * cargo) + (PANEL_PT * panel) + auto + climb