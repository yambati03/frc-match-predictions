import numpy as np
from scipy.stats import truncnorm
from tbainfo import tbarequests

CARGO_PT = 3
PANEL_PT = 2
AUTO1 = 3
AUTO2 = 6
CLIMB1 = 3
CLIMB2 = 6
CLIMB3 = 12


# returns a normal distribution truncated at the specified min and max
def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


# returns the mean value of randomly chosen points from a distribution
def get_predicted_mean(data, num_points):
    mu, sigma, max, min = np.mean(data), np.std(data), float(np.max(data)), float(np.min(data))
    s = get_truncated_normal(mu, sigma, min, max).rvs(num_points)
    mean = np.mean(s)
    return mean


def run_sim(match_id, competition, match_cutoff, db):
    competition_id = db.get_competition_id(competition)
    tba = tbarequests('jQusM2aYtJLHXv3vxhDcPpIWzaxjMga5beNRWOarv6wdRwTF63vNpIsLYVANvCWE')
    alliances = tba.get_match_teams(str(match_id))
    predicted_score = []

    for alliance in alliances:

        points = 0
        taken_L3 = False
        start_L2 = 0

        for team in alliance:

            team_id = db.get_team_id(team)
            matches_team_ids = db.get_matches_team_id(team_id, competition_id, match_cutoff)
            cargo = get_predicted_mean(db.get_metric(matches_team_ids, "'Cargo'"), 1000)
            panel = get_predicted_mean(db.get_metric(matches_team_ids, "'Panel'"), 1000)

            print(db.get_auto_metric(matches_team_ids, 'endgame'))
            points += (CARGO_PT * cargo) + (PANEL_PT * panel) #+ auto + climb

        predicted_score.append(points)

    return predicted_score
