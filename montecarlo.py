import numpy as np
from scipy.stats import truncnorm
from tbainfo import tbarequests
from team import SimTeam
import globals

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
def get_dist(data, num_points):
    mu, sigma, max, min = np.mean(data), np.std(data), float(np.max(data)), float(np.min(data))
    if mu == 0:
        return 0
    if max == min:
        return mu
    s = get_truncated_normal(mu, sigma, min, max).rvs(num_points)

    return list(s)


def create_team_objs(alliance, db):

    objs = []

    for team in alliance:

        team_id = db.get_team_id(team)
        matches_team_ids = db.get_matches_team_id(team_id, db.get_competition_id(globals.competition), globals.match_cutoff)
        team_obj = SimTeam(team_id, team, matches_team_ids)

        team_obj.cargo = get_dist(db.get_metric(matches_team_ids, "'Cargo'", 'false'), 100000)
        team_obj.panel = get_dist(db.get_metric(matches_team_ids, "'Panel'", 'false'), 100000)

        team_obj.cargo_auto = get_dist(db.get_metric(matches_team_ids, "'Cargo'", 'true'), 100000)
        team_obj.panel_auto = get_dist(db.get_metric(matches_team_ids, "'Panel'", 'true'), 100000)

        team_obj.populate_endgame_auto(db.get_status(matches_team_ids, 'endgame'), db.get_status(matches_team_ids, 'auto'))

        objs.append(team_obj)

    return objs


#  returns predicted endgame points
def compute_endgame_points(team_objs):
    L3_team = []
    L2_teams = []
    L1_teams = []

    # loop through teams and predict endgame statuses based on likelihood of a certain climb level
    for team in team_objs:
        # append team if space
        if L3_team == [] and team.status == 'L3':
            L3_team.append(team)
        elif len(L2_teams) < 2 and team.status == 'L2':
            L2_teams.append(team)
        elif len(L1_teams) < 3 and team.status == 'L1':
            L1_teams.append(team)
        # if no space, only append to a climb level if likelihood is greater
        # than previously assigned team and move the team down a climb level
        else:
            sorted(L2_teams, key=lambda x: x.L2)
            sorted(L1_teams, key=lambda x: x.L1)
            if team.status == 'L3' and team.L3 > L3_team[0].L3:
                L2_teams.append(L3_team[0])
                del L3_team[0]
                L3_team.append(team)
                if len(L2_teams) > 2:
                    sorted(L2_teams, key=lambda x: x.L2)
                    L1_teams.append(L2_teams[-1])
                    del L2_teams[-1]
            if team.status == 'L2' and team.L2 > L2_teams[0].L2:
                L2_teams.append(team)
                sorted(L2_teams, key=lambda x: x.L2)
                L1_teams.append(L2_teams[-1])
                del L2_teams[-1]
            else:
                L1_teams.append(team)

    return (len(L3_team) * CLIMB3) + (len(L2_teams) * CLIMB2) + (len(L1_teams) * CLIMB1)


# returns predicted auto points for hab line crossing only
def compute_auto_hab_points(team_objs):
    L2_teams = []
    L1_teams = []

    # if no space, only append to a starting level if likelihood is greater
    # than previously assigned team and move the team down a starting level
    for team in team_objs:
        if team.auto_status == -1:
            continue
        if len(L2_teams) < 2 and team.auto_status == 'L2':
            L2_teams.append(team)
        elif len(L1_teams) < 3 and team.auto_status == 'L1':
            L1_teams.append(team)
        else:
            sorted(L2_teams, key=lambda x: x.L2)
            sorted(L1_teams, key=lambda x: x.L1)
            if team.auto_status == 'L2' and team.L2 > L2_teams[0].L2:
                L2_teams.append(team)
                sorted(L2_teams, key=lambda x: x.L2)
                L1_teams.append(L2_teams[-1])
                del L2_teams[-1]
            else:
                L1_teams.append(team)

    return (len(L2_teams) * AUTO2) + (len(L1_teams) * AUTO1)

def run_sim(match_id, db):
    globals.init()
    tba = tbarequests('jQusM2aYtJLHXv3vxhDcPpIWzaxjMga5beNRWOarv6wdRwTF63vNpIsLYVANvCWE')
    alliances = tba.get_match_teams(str(match_id))
    predicted_score = []

    for alliance in alliances:

        pos = []
        team_objs = create_team_objs(alliance, db)

        for i in range(1000):

            panel = 0
            cargo = 0
            panel_auto = 0
            cargo_auto = 0
            points = 0

            for team in team_objs:

                # add a teams' predicted score contribution to the overall alliance score
                cargo += team.get_rand_cargo()
                panel += team.get_rand_panel()

                cargo_auto += team.get_rand_auto_cargo()
                panel_auto += team.get_rand_auto_panel()

            points += (CARGO_PT * cargo) + (PANEL_PT * panel) + (CARGO_PT * cargo_auto) + (PANEL_PT * panel_auto) + \
                compute_endgame_points(team_objs) + \
                compute_auto_hab_points(team_objs)

            pos.append(points)

        predicted_score.append([np.mean(pos), np.std(pos)])

    return predicted_score
