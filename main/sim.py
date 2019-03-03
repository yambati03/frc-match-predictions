from tbainfo import tbarequests
import montecarlo
import json
from db import dbtools


def main():
    db = dbtools("2019Scouting", "frc900", "frc900")
    tba = tbarequests('jQusM2aYtJLHXv3vxhDcPpIWzaxjMga5beNRWOarv6wdRwTF63vNpIsLYVANvCWE')
    with open('params.json') as f:
        data = json.load(f)
    accuracy = []
    for i in range(int(data['match_cutoff']) + 1, tba.get_all_matches(data['tba_competitionid'], 1)[-1] + 1):
        score = montecarlo.run_sim(data['tba_competitionid'] + '_qm' + str(i), data['competition'], int(data['match_cutoff']), db)
        win = ''
        if score[0] > score[1]:
            win = 'BLUE WINS'
        else:
            win = 'RED WINS'
        accuracy.append(compute_accuracy(win, tba, data['tba_competitionid'] + '_qm' + str(i)))
        print('match number: ' + str(i) + ' --> blue: ' + str(score[0]) + ' // red: ' + str(score[1]) + ' -->' + ' ' + win)
    print(accuracy.count(1)/len(accuracy) * 100)


def compute_accuracy(win, tba, match_id):
    if win.strip(' WINS').lower() == tba.get_winning_alliance(match_id):
        return 1
    else:
        return -1


main()
