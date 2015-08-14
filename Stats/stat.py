#!/usr/bin/env python

import unirest
import json
from sunshine4py import sunshineexceptions

class SunshineStats:
    def setStats(self, data):
        for key, value in data.items():
            if isinstance(value, list) and key == 'data':
                for item in value:
                    try:
                        self.stats[str(item['player'])] = {}
                        key_name = str(item['player'])
                        self.players.append(key_name)
                        for attr, val in item.items():
                            self.stats[key_name][str(attr)] = val
                    except Exception as e:
                        print 'Error adding item to stats dictionary, %s' %  str(e)

    def __init__(self, urls):
        stats_data, self.return_code = json.loads(
                     json.dumps(unirest.get(urls[0], headers={"Accept":"application/json"}).body
                     )), unirest.get(urls[0]).code
        if not str(self.return_code).startswith('2'):
            raise sunshineexceptions.SunshineError(self.return_code)
        for url in urls:
            self.return_code = unirest.get(url).code
            if not str(self.return_code).startswith('2'):
                raise sunshineexceptions.SunshineError(self.return_code)
            stats_data['data'] += json.loads(
                         json.dumps(unirest.get(url, headers={"Accept":"application/json"}).body
                         ))['data']
        self.stats = {}
        self.players = []
        self.setStats(stats_data)
