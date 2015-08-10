#!/usr/bin/env python

import unirest

class SunshinePlayer:
    def __init__(self, name, url):
        self.playerdata = unirest.get(url, header={"Content-Type":"application/json"})
        return self.playerdata
