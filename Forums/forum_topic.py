#!/usr/bin/env python

import json
import unirest
from sunshine4py import sunshineexceptions

class SunshineTopicPost:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.timestamp = data['timestamp']
        self.author = data['author']
        try:
            self.quoting = data['quoting']
        except KeyError:
            pass
class SunshineTopic:
    def setTopicAttributes(self, data):
        for key, value in data.items():
            if key == 'data':
                for attr, val in value.items():
                    setattr(self, attr, val)
                    if attr == 'posts':
                        for item in val:
                            setattr(self, 'p' + item['id'], SunshineTopicPost(item))
    def __init__(self, urls):
        if len(urls) == 1:
            url = urls[0]
            self.topic_data, self.return_code = \
            unirest.get(url, headers={"Accept":"application/json"}).body, \
            unirest.get(url).code
            if not str(self.return_code).startswith('2'):
                raise sunshineexceptions.SunshineError(self.return_code)
            self.setTopicAttributes(self.topic_data)
        elif len(urls) > 1:
            self.topic_data, self.return_code = \
            unirest.get(urls[0], headers={"Accept":"application/json"}).body, \
            unirest.get(urls[0]).code
            if not str(self.return_code).startswith('2'):
                raise sunshineexceptions.SunshineError(self.return_code)
            for url in urls:
                self.return_code = unirest.get(url).code
                if not str(self.return_code).startswith('2'):
                    raise sunshineexceptions.SunshineError(self.return_code)
                self.topic_data['data']['posts'] += unirest.get(url, headers={"Accept":"application/json"}).body['data']['posts']
            self.setTopicAttributes(self.topic_data)
