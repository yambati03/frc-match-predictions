class Team:
    def __init__(self, tba_id, db_id):
        self.tba_id = tba_id
        self.db_id = db_id
        self.cargo = 0
        self.cargo_zscore = 0
        self.panel = 0
        self.panel_zscore = 0
        self.endgame = []
        self.endgame_score = 0
        self.L3 = 0
        self.L2 = 0
        self.L1 = 0

    def get_tba_id(self):
        return self.team_id

    def get_db_id(self):
        return self.db_id


class SimTeam:
    def __init__(self, db_id, endgame, auto):
        self.db_id = db_id
        if len(endgame) > 0:
            self.L3 = endgame.count('Level 3') / len(endgame)
            self.L2 = endgame.count('Level 2') / len(endgame)
            self.L1 = endgame.count('Level 1') / len(endgame)
        else:
            self.L3, self.L2, self.L1 = 0, 0, 0
        self.status = self.get_predicted_endgame()
        if len(auto) > 0:
            self.auto_L2 = auto.count('Level 2') / len(auto)
            self.auto_L1 = auto.count('Level 1') / len(auto)
        else:
            self.auto_L2, self.auto_L1 = 0, 0
        self.auto_status = self.get_predicted_auto()

    def get_db_id(self):
        return self.db_id

    def get_predicted_endgame(self):
        if self.L3 > self.L2 and self.L3 > self.L1 and self.L3 > 0.43:
            return 'L3'
        elif self.L2 > self.L1 and self.L2 > self.L3:
            return 'L2'
        else:
            return 'L1'

    def get_predicted_auto(self):
        if self.auto_L2 > self.auto_L1:
            return 'L2'
        elif self.auto_L1 > self.auto_L2:
            return 'L1'
        else:
            return -1
