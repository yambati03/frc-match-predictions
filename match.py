CARGO_PT = 3
PANEL_PT = 2
AUTO1 = 3
AUTO2 = 6
CLIMB1 = 3
CLIMB2 = 6
CLIMB3 = 12


class TeamScore:
    def __init__(self):
        self.t_cargo = 0
        self.t_panel = 0
        self.a_cargo = 0
        self.a_panel = 0
        self.total_cargo = 0
        self.total_panel = 0
        self.auto_hab = ''
        self.endgame = ''

    def sum_vars(self):
        self.total_cargo = self.t_cargo + self.a_cargo
        self.total_panel = self.t_panel + self.a_panel


class AllianceScore:
    def __init__(self, color):
        self.color = color
        self.team1 = TeamScore()
        self.team2 = TeamScore()
        self.team3 = TeamScore()
        self.score = 0
        self.cargo = 0
        self.panel = 0
        self.auto_L1 = 0
        self.auto_L2 = 0
        self.endgame_L1 = 0
        self.endgame_L2 = 0
        self.endgame_L3 = 0

    def compute_vars(self):
        self.cargo = self.team1.total_cargo + self.team2.total_cargo + self.team3.total_cargo



class Match:

    def __init__(self, alliances, match_id, red_score, blue_score):
        self.match_id = match_id
        self.blue_teams = alliances[0]
        self.red_teams = alliances[1]
        self.red_score = AllianceScore('red')
        self.blue_score = AllianceScore('blue')


