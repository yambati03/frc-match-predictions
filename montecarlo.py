import numpy as np
import scipy.stats as stats
from tbainfo import tbarequests
from sim_team import SimTeam
from match_score import Match
from match_score import TeamScore
from match_score import AllianceScore
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
    return stats.truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


# returns the mean value of randomly chosen points from a distribution
def get_dist(data, num_points):
    mu, sigma, max, min = np.mean(data), np.std(data), float(np.max(data)), float(np.min(data))
    if mu == 0:
        return 0
    if max == min:
        return mu
    s = get_truncated_normal(mean=mu, sd=sigma, low=min, upp=max).rvs(num_points)
    return list(s)


# generate objects for each given team and populate with distributed data points
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


# returns predicted endgame points
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


def run_sim(db, match_id=-1, alliances=-1):
    globals.init()
    tba = tbarequests('jQusM2aYtJLHXv3vxhDcPpIWzaxjMga5beNRWOarv6wdRwTF63vNpIsLYVANvCWE')
    if match_id != -1:
        alliances = tba.get_match_teams(str(match_id))
    else:
        pass

    predicted_score = []

    for alliance in alliances:

        team_objs = create_team_objs(alliance, db)

        alliancescore = AllianceScore(alliance)
        team_scores = []

        for team in team_objs:

            # add a teams' predicted score contribution to the overall alliance score
            cargo = np.mean(team.cargo)
            panel = np.mean(team.panel)

            cargo_auto = np.mean(team.cargo_auto)
            panel_auto = np.mean(team.panel_auto)

            teamscore = TeamScore(team.tba_id, cargo, panel, cargo_auto, panel_auto)

            teamscore.sum_vars()

            team_scores.append(teamscore)

        alliancescore.team1 = team_scores[0]
        alliancescore.team2 = team_scores[1]
        alliancescore.team3 = team_scores[2]
        alliancescore.sum_vars()
        alliancescore.totalscore += compute_endgame_points(team_objs) + compute_auto_hab_points(team_objs)

        predicted_score.append(alliancescore)

    match = Match(predicted_score[0], predicted_score[1], match_id)

    return match
