import requests
import json

TBA_AUTH_KEY = "jQusM2aYtJLHXv3vxhDcPpIWzaxjMga5beNRWOarv6wdRwTF63vNpIsLYVANvCWE"
headers = {'X-TBA-Auth-Key': TBA_AUTH_KEY}


def get_teams(comp_id):
    teams = requests.get('https://www.thebluealliance.com/api/v3/event/' + comp_id + '/teams/keys', headers=headers)
    return teams.json()


def get_team_matches(comp_id, team):
    matches = requests.get('https://www.thebluealliance.com/api/v3/team/' + team + '/event/' + comp_id + '/matches/keys', headers=headers)
    return matches.json()


def get_all_matches(comp_id):
    matches = requests.get('https://www.thebluealliance.com/api/v3/event/' + comp_id + '/matches/keys', headers=headers)
    return matches.json()


def get_match_score(match_id, alliance):
    data = requests.get('https://www.thebluealliance.com/api/v3/match/' + match_id + '/simple', headers=headers)
    return data.json()['alliances'][alliance]['score']

print(get_match_score('2018nccmp_qm2','red'))
