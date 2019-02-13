from tbainfo import tbarequests
from db import dbtools
import numpy as np
import matplotlib.pyplot as plt
import json

db = dbtools("2018Scouting", "frc900", "frc900")
competition_id = db.get_competition_id("'District Champs'")
tba = tbarequests('jQusM2aYtJLHXv3vxhDcPpIWzaxjMga5beNRWOarv6wdRwTF63vNpIsLYVANvCWE')
teams = tba.get_teams('2018nccmp')

scaling_ability = []
switch_ability = []
win_p = []

with open('main\params.json') as f:
    data = json.load(f)

for team in teams:
    team_id = db.get_team_id(team)
    matches_team_ids = db.get_matches_team_id(str(team_id), str(competition_id), int(data['match_cutoff']))
    scale = np.mean(db.get_metric(matches_team_ids, "'Scale'"))
    scaling_ability.append(scale)
    switch = db.get_metric(matches_team_ids, "'Switch'")
    cswitch = db.get_metric(matches_team_ids, "'Counter-Switch'")
    fswitch = [x + y for x, y in zip(switch, cswitch)]
    switch = np.mean(fswitch)
    switch_ability.append(switch)
    win_p.append(tba.get_wins('2018nccmp', team))
    print('processing... ' + str((teams.index(team)/len(teams))*100) + '%')

fig, ax = plt.subplots()
ax.scatter(scaling_ability, win_p)
ax.scatter(switch_ability, win_p)

for i, txt in enumerate(teams):
    ax.annotate(txt, (scaling_ability[i], win_p[i]))

plt.show()



