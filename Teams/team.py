#!/usr/bin/env python

import unirest
import json
from sunshine4py.sunshineexceptions import checkCode

class SunshineTeamPlayer:
    def __init__(self, data):
        for key, val in data.items():
            setattr(self, key, val)

class SunshineTeam:
    def setTeamAttributes(self, data):
        for key, val in data.items():
            if key == 'stats':
                for attr, value in val.items():
                    setattr(self, attr, value)
            elif key != 'players':
                setattr(self, key, val)
            elif key == 'players':
                for player in val:
                    for attr in player:
                        setattr(self, str(player['username']), SunshineTeamPlayer(player))
    def __init__(self, url):
        self.url = url
        self.parsed_data, self.return_code = unirest.get(self.url).body['data'], unirest.get(self.url).code
        checkCode(self.return_code)
        self.setTeamAttributes(self.parsed_data)
