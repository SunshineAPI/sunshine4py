#!/usr/bin/env python

import unirest
import json
from sunshine4py import sunshineexceptions

class SunshineStats:
    def setStats(self, data):
        for key, value in data.items():
            if isinstance(value, list) and key == 'data':
                for item in value:
                    print item
                    try:
                        self.stats[str(item['player'])] = {}
                        key_name = str(item['player'])
                        for attr, val in item.items():
                            self.stats[key_name][str(attr)] = val
                    except Exception as e:
                        print 'Error adding item to stats dictionary, %s' %  str(e)

    def __init__(self, urls):
        stats_data = json.loads(
                     json.dumps(unirest.get(urls[0], headers={"Accept":"application/json"}).body
                     ))
        for url in urls:
            stats_data['data'] += json.loads(
                         json.dumps(unirest.get(url, headers={"Accept":"application/json"}).body
                         ))['data']
        self.stats = {}
        self.setStats(stats_data)
