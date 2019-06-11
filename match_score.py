CARGO_PT = 3
PANEL_PT = 2
AUTO1 = 3
AUTO2 = 6
CLIMB1 = 3
CLIMB2 = 6
CLIMB3 = 12


class TeamScore:
    def __init__(self, team_id, t_cargo, t_panel, a_cargo, a_panel):
        self.team_id = team_id
        self.t_cargo = t_cargo
        self.t_panel = t_panel
        self.a_cargo = a_cargo
        self.a_panel = a_panel
        self.total_cargo = 0
        self.total_panel = 0
        self.total = 0
        self.auto_hab = ''
        self.endgame = ''

    def sum_vars(self):
        self.total_cargo = self.t_cargo + self.a_cargo
        self.total_panel = self.t_panel + self.a_panel
        self.total = self.total_cargo + self.total_panel


class AllianceScore:
    def __init__(self, teams):
        self.teams = teams
        self.team1 = None
        self.team2 = None
        self.team3 = None
        self.score = 0
        self.cargo = 0
        self.panel = 0
        self.auto_L1 = 0
        self.auto_L2 = 0
        self.endgame_L1 = 0
        self.endgame_L2 = 0
        self.endgame_L3 = 0
        self.totalscore = 0

    def sum_vars(self):
        self.cargo = self.team1.total_cargo + self.team2.total_cargo + self.team3.total_cargo
        self.panel = self.team1.total_panel + self.team2.total_panel + self.team3.total_panel
        self.totalscore += self.cargo + self.panel


class Match:
    def __init__(self, blue, red, match_id):
        self.match_id = match_id
        self.red = red
        self.blue = blue


