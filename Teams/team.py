#!/usr/bin/env python

import unirest
import json
from sunshine4py import sunshineexceptions

class SunshineTeams:
    def setTeamList(self, data):
        for key, value in data.items():
            if isinstance(value, list) and key == 'data':
                for team in value:
                    for attr in team:
                        if str(attr) == 'id':
                            self.teams[team[attr]] = {}
                            team_name = str(team[attr])
                        else:
                            self.teams[team_name][str(attr)] = team[attr]
    def __init__(self, urls):
        print urls
        self.teams_data = json.dumps(unirest.get(urls[0],  headers={'Accept':'application/json'}).body)
        self.parsed_data = json.loads(self.teams_data)
        for url in urls:
            if urls.index(url) == 0:
                pass
            else:
                self.parsed_data['data'] += json.loads(json.dumps(unirest.get(url, headers={'Accept':'application/json'}).body))['data']
        self.teams = {}
        self.setTeamList(self.parsed_data)
    def __repr__(self):
        return self.teams
