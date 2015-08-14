#!/usr/bin/env pyton

import unirest
import json
from sunshine4py import sunshineexceptions

class SunshineTournament:
    def setTournamentAttributes(self, data):
        for key, value in data.items():
            if isinstance(value, dict) and not key == 'info':
                self.setTournamentAttributes(value)
            if isinstance(value, dict) and key == 'info':
                for attr, val in value.items():
                    setattr(self, attr, val)
            if isinstance(value, list):
                setattr(self, 'teams', value)
    def __init__(self, url):
        self.url = url
        self.tournament_data, self.return_code = \
            json.dumps(unirest.get(url, headers={"Accept":"application/json"}).body), \
            unirest.get(url).code
        if not str(self.return_code).startswith('2'):
            raise sunshineexceptions.SunshineError(self.return_code)
        self.parsed_data = json.loads(self.tournament_data)
        self.setTournamentAttributes(self.parsed_data)
