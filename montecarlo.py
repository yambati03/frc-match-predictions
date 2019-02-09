import numpy as np
from scipy.stats import truncnorm

CARGO_PT = 3
PANEL_PT = 2
AUTO1 = 3
AUTO2 = 6
CLIMB1 = 3
CLIMB2 = 6
CLIMB3 = 12


def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


def main():

    points = 0
    counter = 0
    for i in all:
        counter += 1
        mu, sigma, max, min = np.mean(i), np.std(i), float(np.max(i)), float(np.min(i))
        if sigma == 0:
            points += i[0]
        else:
            s = get_truncated_normal(mu,sigma,min,max).rvs(10)
            mean = np.mean(s)
            points += mean * (counter - 1)

    print('final:' + str(points))

main()