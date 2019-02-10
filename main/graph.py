from tbainfo import tbarequests
from db import dbtools
import numpy as np
import matplotlib.pyplot as plt

db = dbtools("2018Scouting", "frc900", "frc900")
competition_id = db.get_competition_id("'District Champs'")
tba = tbarequests('jQusM2aYtJLHXv3vxhDcPpIWzaxjMga5beNRWOarv6wdRwTF63vNpIsLYVANvCWE')
teams = tba.get_teams('2018nccmp')

scaling_ability = []
switch_ability = []
win_p = []

for team in teams:
    team_id = db.get_team_id(team)
    matches_team_ids = db.get_matches_team_id(str(team_id), str(competition_id))
    scale = np.mean(db.get_metric(matches_team_ids, "'Scale'"))
    scaling_ability.append(scale)
    switch = np.mean(db.get_metric(matches_team_ids, "'Switch'"))
    switch_ability.append(switch)
    win_p.append(tba.get_wins('2018nccmp', team))
    print('processing... ' + str((teams.index(team)/len(teams))*100) + '%')

plt.scatter(scaling_ability, win_p)
plt.scatter(switch_ability, win_p)
plt.show()



