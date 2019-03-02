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