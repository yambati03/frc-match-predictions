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


def sort_dict(dict, cutoff):
    sorted_x = sorted(dict.items(), key=lambda kv: kv[1])
    sorted_x = [x[0] for x in sorted_x if x[1] > cutoff]
    return sorted_x


# returns predicted endgame points
def get_endgame(team_objs):
    L1 = {}
    L2 = {}
    L3 = {}

    statuses = {}

    for team in team_objs:
        statuses[team.tba_id] = ''
        L1[team.tba_id] = team.endgame_status.get('L1')
        L2[team.tba_id] = team.endgame_status.get('L2')
        L3[team.tba_id] = team.endgame_status.get('L3')

    L1 = sort_dict(L1, 0.1)
    L2 = sort_dict(L2, 0.15)
    L3 = sort_dict(L3, 0.2)

    for id in L1:
        statuses[id] = 'L1'

    for i, id in enumerate(L2):
        if i > 1:
            break
        statuses[id] = 'L2'

    for i, id in enumerate(L3):
        if i > 0:
            break
        statuses[id] = 'L3'

    return statuses


# returns predicted auto points for hab line crossing only
def get_auto(team_objs):
    L1 = {}
    L2 = {}

    statuses = {}

    for team in team_objs:
        statuses[team.tba_id] = ''
        L1[team.tba_id] = team.auto_status.get('L1')
        L2[team.tba_id] =  team.auto_status.get('L2')

    L1 = sort_dict(L1, 0.1)
    L2 = sort_dict(L2, 0.15)

    for id in L1:
        statuses[id] = 'L1'

    for i, id in enumerate(L2):
        if i > 1:
            break
        statuses[id] = 'L2'

    return statuses


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
        team_scores = []
        endgame = get_endgame(team_objs)
        auto = get_auto(team_objs)

        for team in team_objs:

            # add a teams' predicted score contribution to the overall alliance score
            cargo = np.mean(team.cargo)
            panel = np.mean(team.panel)

            cargo_auto = np.mean(team.cargo_auto)
            panel_auto = np.mean(team.panel_auto)

            teamscore = TeamScore(team.tba_id, cargo, panel, cargo_auto, panel_auto, auto.get(team.tba_id), endgame.get(team.tba_id))

            team_scores.append(teamscore)

        alliancescore = AllianceScore(team_scores[0], team_scores[1], team_scores[2])

        predicted_score.append(alliancescore)

    match = Match(predicted_score[0], predicted_score[1], match_id)

    return match
