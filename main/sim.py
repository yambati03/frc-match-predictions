from tbainfo import tbarequests
import montecarlo
from db import dbtools
import globals


# predicts match outcome for all matches after a given match cutoff
def main():
    globals.init()
    db = dbtools("Wake", "frc900", "frc900")
    tba = tbarequests('jQusM2aYtJLHXv3vxhDcPpIWzaxjMga5beNRWOarv6wdRwTF63vNpIsLYVANvCWE')
    accuracy = []

    # loop through matches and run a simulation for each
    for i in range(globals.match_cutoff + 1, tba.get_all_matches(globals.tba_competition_id, 1)[-1] + 1):
        score = montecarlo.run_sim(db, match_id=globals.tba_competition_id + '_qm' + str(i))
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

# predicts the outcome of a single match
def sim_match(match_id):
    db = dbtools("Wake", "frc900", "frc900")
    score = montecarlo.run_sim(db, match_id=match_id)
    win = ''
    if score[0][0] > score[1][0]:
        win = 'BLUE WINS'
    else:
        win = 'RED WINS'
    print('match number: ' + match_id + ' --> red: ' + str(score[1][0]) + ' std: ' + str(round(score[1][1], 2)) + ' // blue: ' + str(score[0][0]) + ' std: ' + str(round(score[0][1], 2)) + ' -->' + ' ' + win)


# predicts match outcome given fabricated alliances - argument should be in form [[team, team, team],[team, team, team]]
def sim_alliances(alliances):
    db = dbtools("Wake", "frc900", "frc900")
    score = montecarlo.run_sim(db, alliances=alliances)
    win = ''
    if score[1][0] > score[0][0]:
        win = 'BLUE WINS'
    else:
        win = 'RED WINS'
    print('red: ' + str(score[0][0]) + ' std: ' + str(round(score[0][1], 2)) + ' // blue: ' + str(score[1][0]) + ' std: ' + str(round(score[1][1], 2)) + ' -->' + ' ' + win)


main()
