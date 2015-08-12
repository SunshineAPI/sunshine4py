#!/usr/bin/env python

from sunshine4py import Players
from sunshine4py import sunshineexceptions
from sunshine4py import Teams
from os.path import join
from Teams.team import SunshineTeams
from Players.player import SunshinePlayer
import json
import urllib
import socket

try:
    from pip import get_installed_distributions
    packages = get_installed_distributions()
    packages_list = sorted(["%s" % (i.key) for i in packages])
    if 'unirest' in packages_list:
        import unirest
except ImportError as e:
    print str(e) + ', Cannot import Unirest, either you don\'t have it installed, \n \
           or it isn\'t installed properly. ' + str(e)
except Exception:
    print 'Unexpected exception'

class Sunshine:
    def __init__(self, server, port):
        self.server = server
        self.port = port
        if not isinstance(server, str):
            raise TypeError("Server address must be str")
        elif not isinstance(port, int):
            if isinstance(port, str):
                try:
                    self.port = int(port)
                except Exception:
                    raise Exception('port number must be an int or str')
            else:
                raise TypeError('port number must be an int or str')
        self.server_connection = socket.socket(socket.AF_INET)
        try:
            self.server_connection.connect((server, port))
            self.ip_addr = socket.gethostbyname(server)
            print self.ip_addr
        except Exception as e:
            print str(e) + ', unable to connect to server'
        self.url = '{0}:{1}'.format(self.server, self.port)
    def getPlayer(self, name):
        player_url = join(self.url, 'players', name)
        return SunshinePlayer(name, player_url)
    def getTeams(self, *page_nums):
        teams_urls = []
        print page_nums
        if len(page_nums) == 1:
            if isinstance(page_nums[0], int):
                teams_urls.append(join('http://', self.url, 'teams', '?page={0}'.format(page_nums[0])))
            elif isinstance(page_nums[0], str):
                if page_nums[0].count('-') == 1:
                    page_range = page_nums[0].split('-')
                    for item in page_range:
                        if not item.isdigit():
                            raise ValueError('Invalid page numbers.')
                            return
                        ind=page_range.index(item)
                        page_range[ind]=int(item)
                    page_range.sort()
                    for i in range(page_range[0], page_range[1]+1):
                        teams_urls.append(join('http://', self.url, 'teams', '?page={0}'.format(i)))
                elif page_nums[0].isdigit():
                    teams_urls.append(join('http://', self.url, 'teams', '?page={0}'.format(page_nums[0])))
                else:
                    raise ValueError('Invalid page number.')
        elif len(page_nums) > 1:
            for item in page_nums:
                if isinstance(item, str):
                    if not item.isdigit():
                        raise ValueError('Invalid page numbers.')
                        return
                if not isinstance(item, int):
                    raise ValueError('Invalid page numbers.')
                    return
                teams_urls.append(join('http://', self.url, 'teams', '?page={0}'.format(str(item))))
        return SunshineTeams(teams_urls)
