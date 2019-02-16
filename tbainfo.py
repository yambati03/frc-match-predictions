import requests


class tbarequests:

    # tbarequests should be initialized with a API key in order to access tba data
    def __init__(self, key):
        self.TBA_AUTH_KEY = key
        self.headers = {'X-TBA-Auth-Key': key}

    # returns a list of all teams at a specified competition
    def get_teams(self, comp_id):
        teams = requests.get('https://www.thebluealliance.com/api/v3/event/' + comp_id + '/teams/keys', headers=self.headers)
        return teams.json()

    # returns all matches that a specified team will compete in at a specified competition
    def get_team_matches(self, comp_id, team):
        matches = requests.get('https://www.thebluealliance.com/api/v3/team/' + team + '/event/' + comp_id + '/matches/keys', headers=self.headers)
        return matches.json()

    # returns tba keys of all matches at a specified competition
    def get_all_matches(self, comp_id, qm):
        matches = requests.get('https://www.thebluealliance.com/api/v3/event/' + comp_id + '/matches/keys', headers=self.headers)
        if not qm:
            return matches.json()
        else:
            return sorted([int(s.replace(comp_id + "_qm", '')) for s in matches.json() if '_qm' in s])

    # returns the final score of a match; if an alliance is specified, will only return that alliance's final score
    def get_match_score(self, match_id, alliance):
        data = requests.get('https://www.thebluealliance.com/api/v3/match/' + match_id + '/simple', headers=self.headers)
        return data.json()['alliances'][alliance]['score']

    # returns the teams competing in a specified match
    def get_match_teams(self, match_id):
        data = requests.get('https://www.thebluealliance.com/api/v3/match/' + match_id + '/simple', headers=self.headers)
        return [data.json()['alliances']['blue']['team_keys'], data.json()['alliances']['red']['team_keys']]

    # returns the winning alliance of a match
    def get_winning_alliance(self, match_id):
        data = requests.get('https://www.thebluealliance.com/api/v3/match/' + match_id + '/simple', headers=self.headers)
        return data.json()['winning_alliance']

    # returns the percentage of matches a specified team won at a specified competition
    def get_wins(self, comp_id, team_id):
        wins = 0
        team_matches = self.get_team_matches(comp_id, team_id)
        for i in team_matches:
            match_teams = self.get_match_teams(i)
            alliance = ''
            if match_teams[0].count(team_id) == 1:
                alliance = 'blue'
            else:
                alliance = 'red'
            winning_alliance = self.get_winning_alliance(i)
            if winning_alliance == alliance:
                wins += 1
        return wins/len(team_matches)

