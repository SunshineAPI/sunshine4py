#!/usr/bin/env python

import unirest
import json
from sunshine4py import sunshineexceptions

class SunshineStats:
    class SunshineStatsPlayer:
        def __init__(self, name, data):
            for key, value in data.items():
                setattr(self, key, value)
    def setStats(self, stats_data):
        for item in stats_data:
            setattr(self, item['name'], self.SunshineStatsPlayer(item['name'], item))
    def __init__(self, urls):
        stats_data, self.return_code = unirest.get(urls[0], headers={"Accept":"application/json"}).body['data'], \
                                       unirest.get(urls[0]).code
        if not str(self.return_code).startswith('2'):
            raise sunshineexceptions.SunshineError(self.return_code)
        for url in urls:
            self.return_code = unirest.get(url).code
            if not str(self.return_code).startswith('2'):
                raise sunshineexceptions.SunshineError(self.return_code)
            if urls.index(url) == 0:
                continue
            stats_data += unirest.get(url, headers={"Accept":"application/json"}).body['data']
        self.setStats(stats_data)
        self.stats = stats_data
        print 'Retreived information for ' + str(len(stats_data)) + ' players.'
