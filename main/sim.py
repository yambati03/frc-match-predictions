from tbainfo import tbarequests
import montecarlo
from db import dbtools
import globals


def main():
    globals.init()
    db = dbtools("Wake", "frc900", "frc900")
    tba = tbarequests('jQusM2aYtJLHXv3vxhDcPpIWzaxjMga5beNRWOarv6wdRwTF63vNpIsLYVANvCWE')
    accuracy = []

    # loop through matches and run a simulation for each
    for i in range(globals.match_cutoff + 1, tba.get_all_matches(globals.tba_competition_id, 1)[-1] + 1):
        score = montecarlo.run_sim(globals.tba_competition_id + '_qm' + str(i), db)
        win = ''
        if score[0][0] > score[1][0]:
            win = 'BLUE WINS'
        else:
            win = 'RED WINS'
        accuracy.append(compute_accuracy(win, tba, globals.tba_competition_id + '_qm' + str(i)))
        print('match number: ' + str(i) + ' --> red: ' + str(score[1][0]) + ' std: ' + str(round(score[1][1], 2)) + ' // blue: ' + str(score[0][0]) + ' std: ' + str(round(score[0][1], 2)) + ' -->' + ' ' + win, tba.get_winning_alliance(globals.tba_competition_id + '_qm' + str(i)))
    print(str(round((accuracy.count(1)/len(accuracy)) * 100, 3)) + '%')


# accuracy is defined as number of correct predictions over the number of predicted matches
def compute_accuracy(win, tba, match_id):
    if win.strip(' WINS').lower() == tba.get_winning_alliance(match_id):
        return 1
    else:
        return -1


def sim_match(match_id):
    db = dbtools("Wake", "frc900", "frc900")
    score = montecarlo.run_sim(match_id, db)
    win = ''
    if score[0][0] > score[1][0]:
        win = 'BLUE WINS'
    else:
        win = 'RED WINS'
    print('match number: ' + match_id + ' --> red: ' + str(score[1][0]) + ' std: ' + str(round(score[1][1], 2)) + ' // blue: ' + str(score[0][0]) + ' std: ' + str(round(score[0][1], 2)) + ' -->' + ' ' + win)


main()
