import requests


class tbarequests:
    def __init__(self, key):
        self.TBA_AUTH_KEY = key
        self.headers = {'X-TBA-Auth-Key': key}

    def get_teams(self, comp_id):
        teams = requests.get('https://www.thebluealliance.com/api/v3/event/' + comp_id + '/teams/keys', headers=headers)
        return teams.json()

    def get_team_matches(self, comp_id, team):
        matches = requests.get('https://www.thebluealliance.com/api/v3/team/' + team + '/event/' + comp_id + '/matches/keys', headers=headers)
        return matches.json()

    def get_all_matches(self, comp_id):
        matches = requests.get('https://www.thebluealliance.com/api/v3/event/' + comp_id + '/matches/keys', headers=headers)
        return matches.json()

    def get_match_score(self, match_id, alliance):
        data = requests.get('https://www.thebluealliance.com/api/v3/match/' + match_id + '/simple', headers=headers)
        return data.json()['alliances'][alliance]['score']

    def get_match_teams(self, match_id):
        data = requests.get('https://www.thebluealliance.com/api/v3/match/' + match_id + '/simple', headers=headers)
        return [data.json()['alliances']['blue']['team_keys'], data.json()['alliances']['red']['team_keys']]