import numpy as np


class Team:
    def __init__(self, tba_id, db_id):
        self.tba_id = tba_id
        self.db_id = db_id
        self.matches = []
        self.cargo = 0
        self.cargo_raw = []
        self.cargo_zscore = 0
        self.panel = 0
        self.panel_raw = []
        self.panel_zscore = 0
        self.auto = []
        self.endgame = []
        self.endgame_score = 0
        self.L3 = 0
        self.L2 = 0
        self.L1 = 0

    def get_tba_id(self):
        return self.team_id

    def get_db_id(self):
        return self.db_id

    def get_predicted_endgame(self):
        if self.L3 >= self.L2 and self.L3 >= self.L1:
            return ['L3', self.L3]
        elif self.L2 >= self.L1 and self.L2 >= self.L3:
            return ['L2', self.L2]
        else:
            return ['L1', self.L1]

    def get_data(self, index):
        return str(index + 1) + ' ' + self.tba_id + \
            '\n \t - ' + 'cargo mean: ' + str(round(self.cargo, 2)) + ' max: ' + str(round(np.max(self.cargo_raw), 2)) + ' min: ' + str(round(np.min(self.cargo_raw), 2)) + \
            '\n \t - ' + 'panel mean: ' + str(round(self.panel, 2)) + ' max: ' + str(round(np.max(self.panel_raw), 2)) + ' min: ' + str(round(np.min(self.panel_raw), 2)) + \
            '\n \t - ' + 'cross hab-line: ' + str(len(self.auto)) + '/' + str(len(self.matches)) + \
            '\n \t - ' + 'common endgame: ' + self.get_predicted_endgame()[0] + ' ' + str(self.get_predicted_endgame()[1]) + '/' + str(len(self.endgame)) + '\n'
