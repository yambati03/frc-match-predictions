import random


class SimTeam:
    def __init__(self, db_id, tba_id, matches_team_ids):
        self.tba_id = tba_id
        self.db_id = db_id
        self.matches_team_ids = []

        self.cargo = []
        self.panel = []
        self.cargo_auto = []
        self.panel_auto = []

        self.endgame_status = {}
        self.auto_status = {}

    def get_db_id(self):
        return self.db_id

    def populate_endgame_auto(self, endgame, auto):
        if len(endgame) > 0:
            self.endgame_status['L3'] = endgame.count('Level 3') / len(endgame)
            self.endgame_status['L2'] = endgame.count('Level 2') / len(endgame)
            self.endgame_status['L1'] =  endgame.count('Level 1') / len(endgame)
        if len(auto) > 0:
            self.auto_status['L2'] = auto.count('Level 2') / len(auto)
            self.auto_status['L1'] = auto.count('Level 1') / len(auto)

    def get_rand_cargo(self):
        if type(self.cargo) != list:
            return 0
        return random.choice(self.cargo)

    def get_rand_panel(self):
        if type(self.panel) != list:
            return 0
        return random.choice(self.panel)

    def get_rand_auto_cargo(self):
        if type(self.cargo_auto) != list:
            return 0
        return random.choice(self.cargo_auto)

    def get_rand_auto_panel(self):
        if type(self.panel_auto) != list:
            return 0
        return random.choice(self.panel_auto)
