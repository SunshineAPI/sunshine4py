#!/usr/bin/env python

import unirest
import json
from sunshine4py import sunshineexceptions

class SunshinePlayer:
    def setPlayerAttributes(self, data):
        for key, value in data.items():
            if key == 'errors':
                raise sunshineexceptions.PlayerError
            if hasattr(self, str(key)):
                setattr(self, str(self.dict_name + '_' + key), value)
            setattr(self, str(key), value)
            if isinstance(value, dict):
                data = value
                self.dict_name = key
                self.setPlayerAttributes(data)

    def __init__(self, name, url):
        self.name = name
        self.player_data, self.return_code = json.dumps(unirest.get('http://' + url, header={"Accept":"application/json"}).body), \
        unirest.get('http://' + url).code
        if not str(self.return_code).startswith('2'):
            raise sunshineexceptions.SunshineError(code)
        parsed_data = json.loads(self.player_data)
        self.dict_name=''
        self.setPlayerAttributes(parsed_data)
