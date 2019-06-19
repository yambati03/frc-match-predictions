CARGO_PT = 3
PANEL_PT = 2
AUTO1 = 3
AUTO2 = 6
CLIMB1 = 3
CLIMB2 = 6
CLIMB3 = 12


class TeamScore:
    def __init__(self, tba_id, t_cargo, t_panel, a_cargo, a_panel, auto, endgame):
        self.tba_id = tba_id
        self.t_cargo = t_cargo
        self.t_panel = t_panel
        self.a_cargo = a_cargo
        self.a_panel = a_panel
        self.total_cargo = self.t_cargo + self.a_cargo
        self.total_panel = self.t_panel + self.a_panel
        self.total = self.total_cargo + self.total_panel
        self.auto = auto
        self.endgame = endgame


class AllianceScore:
    def __init__(self, team1, team2, team3):
        self.team1 = team1
        self.team2 = team2
        self.team3 = team3
        self.cargo = self.team1.total_cargo + self.team2.total_cargo + self.team3.total_cargo
        self.panel = self.team1.total_panel + self.team2.total_panel + self.team3.total_panel
        self.auto_L1 = 0
        self.auto_L2 = 0
        self.endgame_L1 = 0
        self.endgame_L2 = 0
        self.endgame_L3 = 0
        self.auto_endgame()
        self.score = self.cargo + self.panel + self.auto_L1 + self.auto_L2 + self.endgame_L1 + self.endgame_L2 + self.endgame_L3

    def get_team(self, tba_id):
        if self.team1.tba_id == tba_id:
            return self.team1
        elif self.team2.tba_id == tba_id:
            return self.team2
        elif self.team3.tba_id == tba_id:
            return self.team3
        else:
            return -1

    def auto_endgame(self):
        teams = [self.team1, self.team2, self.team3]
        for team in teams:
            if team.auto == 'L1':
                self.auto_L1 += AUTO1
            elif team.auto == 'L2':
                self.auto_L2 += AUTO2

            if team.endgame == 'L1':
                self.endgame_L1 += CLIMB1
            elif team.endgame == 'L2':
                self.endgame_L2 += CLIMB2
            elif team.endgame == 'L3':
                self.endgame_L3 += CLIMB3



class Match:
    def __init__(self, blue, red, match_id):
        self.match_id = match_id
        self.red = red
        self.blue = blue


