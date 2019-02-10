import requests


class tbarequests:
    def __init__(self, key):
        self.TBA_AUTH_KEY = key
        self.headers = {'X-TBA-Auth-Key': key}

    def get_teams(self, comp_id):
        teams = requests.get('https://www.thebluealliance.com/api/v3/event/' + comp_id + '/teams/keys', headers=self.headers)
        return teams.json()

    def get_team_matches(self, comp_id, team):
        matches = requests.get('https://www.thebluealliance.com/api/v3/team/' + team + '/event/' + comp_id + '/matches/keys', headers=self.headers)
        return matches.json()

    def get_all_matches(self, comp_id):
        matches = requests.get('https://www.thebluealliance.com/api/v3/event/' + comp_id + '/matches/keys', headers=self.headers)
        return matches.json()

    def get_match_score(self, match_id, alliance):
        data = requests.get('https://www.thebluealliance.com/api/v3/match/' + match_id + '/simple', headers=self.headers)
        return data.json()['alliances'][alliance]['score']

    def get_match_teams(self, match_id):
        data = requests.get('https://www.thebluealliance.com/api/v3/match/' + match_id + '/simple', headers=self.headers)
        return [data.json()['alliances']['blue']['team_keys'], data.json()['alliances']['red']['team_keys']]

    def get_winning_alliance(self, match_id):
        data = requests.get('https://www.thebluealliance.com/api/v3/match/' + match_id + '/simple', headers=self.headers)
        return data.json()['winning_alliance']

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