#!/usr/bin/env python

import unirest
import json

class SunshinePlayer:
    def setPlayerAttributes(self, data):
        for key, value in data.items():
            setattr(self, str(key), value)
            if isinstance(value, dict):
                data = value
                self.setPlayerAttributes(data)

    def __init__(self, name, url):
        self.player_data = json.dumps(unirest.get('http://' + url, header={"Content-Type":"application/json"}).body)
        parsed_data = json.loads(self.player_data)
        self.setPlayerAttributes(parsed_data)
