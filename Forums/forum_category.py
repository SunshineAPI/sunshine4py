#!/usr/bin/env python
import json
import unirest
from os.path import join
from sunshine4py.Forums.forum_topic import SunshineTopic
from sunshine4py.sunshineexceptions import checkCode

class SunshineForumCategory:
    def setCategoryAttributes(self, data):
        for key, val in data.items():
            if key == 'data':
                for item in val:
                    title = item['title']
                    for char in title:
                        if char == '-':
                            title = title.replace(char, '_')
                        elif not char.isalpha():
                            title = title.replace(char, '')

                    setattr(self, title, SunshineTopic([join('http://', self.server, 'forums', 'topics', item['id'])]))
    def __init__(self, urls, server):
        self.server = server
        if len(urls) == 1:
            url = urls[0]
            self.category_data, self.return_code = \
            unirest.get(url, headers={"Accept":"application/json"}).body, \
            unirest.get(url).code
            checkCode(self.return_code)
            self.setCategoryAttributes(self.category_data)
        elif len(urls) > 1:
            self.category_data, self.return_code = \
            unirest.get(urls[0], headers={"Accept":"application/json"}).body, \
            unirest.get(urls[0]).code
            checkCode(self.return_code)
            for url in urls:
                self.return_code = unirest.get(url).code
                checkCode(self.return_code)
                self.category_data['data'] += unirest.get(url, headers={"Accept":"application/json"}).body['data']
        self.category_topics = self.category_data['data']
        self.setCategoryAttributes(self.category_data)
