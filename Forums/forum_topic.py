#!/usr/bin/env python

import json
import unirest
from sunshine4py.sunshineexceptions import checkCode
from os.path import join

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
        self.reply_url = join('http://', self.url, 'topics', self.id, 'reply')
    def __init__(self, urls, url):
        self.url = url
        self.topic_data, self.return_code = \
        unirest.get(urls[0], headers={"Accept":"application/json"}).body, \
        unirest.get(urls[0]).code
        checkCode(self.return_code)
        self.setTopicAttributes(self.topic_data)
        if len(urls) > 1:
            for url in urls:
                if urls.index(url) == 0: pass
                self.return_code = unirest.get(url).code
                checkCode(self.return_code)
                self.topic_data['data']['posts'] += unirest.get(url, headers={"Accept":"application/json"}).body['data']['posts']
            self.setTopicAttributes(self.topic_data)
