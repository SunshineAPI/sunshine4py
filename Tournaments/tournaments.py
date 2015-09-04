#!/usr/bin/env python

import unirest
import json
from sunshine4py.sunshineexceptions import checkCode

class SunshineTournamentList:
    def setTournamentsAttributes(self, data):
        for key, value in data.items():
            if key == 'data':
                for attr, val in value.items():
                    if attr == 'current':
                        setattr(self, attr, val)
                    elif attr == 'past':
                        for attribute in val:
                            self.past[attribute['link'].replace('/tournaments/', '')] = attribute
    def __init__(self, url):
        self.tournaments_data, self.return_code = json.dumps(unirest.get(url, headers={"Accept":"application/json"}).body), \
        unirest.get(url).code
        checkCode(self.return_code)
        self.parsed_data = json.loads(self.tournaments_data)
        self.past = {}
        self.setTournamentsAttributes(self.parsed_data)
