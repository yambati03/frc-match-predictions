from tbainfo import tbarequests
import montecarlo
import json


def main():
    tba = tbarequests('jQusM2aYtJLHXv3vxhDcPpIWzaxjMga5beNRWOarv6wdRwTF63vNpIsLYVANvCWE')
    with open('params.json') as f:
        data = json.load(f)
    for i in range(data['match_cutoff'], tba.get_all_matches(data['competition'])[-1]):
        score = montecarlo.run_sim(i)
        win = ''
        if score[0] > score[1]:
            win = ' BLUE WINS'
        else:
            win = ' RED WINS'
        print('match number: ' + i + ' --> blue: ' + score[0] + ' // red: ' + score[1] + '-->' + win)


main()
