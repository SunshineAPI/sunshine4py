#!/usr/bin/env python

"""This is a Python package which is a wrapper for the
SunshineAPI (http://github.com/SunshineAPI). To use it,
create an instance of the class Sunshine to retrieve
information from a Sunshine server."""
import sys
from os.path import expanduser

if 'pypy' in sys.prefix:
    print 'It has been detected you are using pypy. Adding Python \n \
    site packages to sys.path...'
    sys.path.append('/usr/lib/python2.7/dist-packages')
    sys.path.append(expanduser('~') + '/.local/lib/python2.7/site-packages')
    sys.path.append(expanduser('~') + '/.local/lib/python2.7/dist-packages')

from pip import get_installed_distributions, main

try:
    packages = get_installed_distributions()
    packages_list = sorted(("%s" % (i.key) for i in packages))
    if 'unirest' in packages_list:
        import unirest
    else:
        raise ImportError
except ImportError as e:
    print 'You do not have unirest installed. Attempting to install unirest...'
    try:
        main(['install', 'unirest'])
    except Exception as e:
        print 'Failed to install unirest. Try installing it manually with \n \
        `pip install unirest`'
        print str(e)

except Exception:
    print 'Unexpected exception'


from sunshine4py import Players
from sunshine4py import sunshineexceptions
from sunshine4py import Teams
from sunshine4py import Stats
from sunshine4py import Tournaments
from sunshine4py import Forums
from os.path import join
from Teams.teams import SunshineTeams
from Teams.team import SunshineTeam
from Players.player import SunshinePlayer
from Stats.stat import SunshineStats
from Tournaments.tournament import SunshineTournament
from Tournaments.tournaments import SunshineTournamentList
from Forums.forum_topic import SunshineTopic
import json
import urllib
import socket

class Sunshine:
    """Sunshine class. To create an instance of this class, execute
    sunshine4py.Sunshine(). If you pass in no arguments, it creates
     an instance from your localhost at port 3000. You can pass in
    arguments to create an instance of the Sunshine class from
    A different server. To do this, simply pass in the arguments
    either the IP address of your server, or the domain name.
    ex. sunshine4py.Sunshine('sunshine-api.com', 80)
    (Without the http://.)"""
    def __init__(self, server='localhost', port=3000):
        self.server = server
        self.port = port
        socket.setdefaulttimeout(1)
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
        except Exception as e:
            raise sunshineexceptions.SunshineError(404)
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
    def getStats(self, *page_nums):
        url_list = []
        if len(page_nums) > 1:
            for i in page_nums:
                assert isinstance(i, int)
        elif len(page_nums) == 1:
            page_nums_list = []
            page_range = []
            assert isinstance(page_nums[0], int) or isinstance(page_nums[0], str)
            page_nums = str(page_nums[0])
            if isinstance(page_nums, str):
                if page_nums.count(',') >= 1:
                    page_nums_list = page_nums.split(',')
                    for i in page_nums_list:
                        assert i.isdigit()
                elif page_nums.count('-') == 1:
                    page_range = page_nums.split('-')
                    assert len(page_range) == 2
                    for i in page_range:
                        assert i.isdigit()
                        page_range[page_range.index(i)] = int(i)
            if page_nums_list:
                for i in page_nums_list:
                    url_list.append(join('http://', self.url, 'stats',
                        '?page={0}'.format(i)))
            elif page_range:
                for i in range(int(page_range[0]), int(page_range[1])+1):
                    url_list.append(join('http://', self.url, 'stats',
                        '?page={0}'.format(i)))
            elif len(page_range) == 0 and len(page_nums_list) == 0:
                for i in page_nums:
                    url_list.append(join('http://', self.url, 'stats',
                        '?page={0}'.format(i)))
        return SunshineStats(url_list)
    def getTournament(self, name):
        if name.count(' ') >= 1:
            name = '-'.join(name.split()).lower()
        else:
            name = name.lower()
        url = join('http://', self.url, 'tournaments', name)
        return SunshineTournament(url)
    def getTournamentList(self):
        return SunshineTournamentList(join('http://', self.url, 'tournaments'))
    def getAuth(self, email, password):
        self.return_code = unirest.post(join('http://', self.url, 'players', 'auth'),
            headers={"Content-Type":"application/json", "Authorization":"Basic","Accept":"application/json"},
            params=json.dumps({"email":"{0}".format(email),"password":"{0}".format(password)})).code
        if not str(self.return_code).startswith('2'):
            raise sunshineexceptions.SunshineError(self.return_code)
        else:
            return str(unirest.post(join('http://', self.url, 'players', 'auth'),
                headers={"Content-Type":"application/json", "Authorization":"Basic","Accept":"application/json"},
                params=json.dumps({"email":"{0}".format(email),"password":"{0}".format(password)})).body['token'])
    def getAlerts(self, auth_token):
        self.return_code = unirest.get(join('http://', self.url, 'alerts'),headers={"Authorization":"Bearer {0}".format(auth_token)}).code
        if not str(self.return_code).startswith('2'):
            raise sunshineexceptions.SunshineError(self.return_code)
        else:
            return unirest.get(join('http://', self.url, 'alerts'),
                    headers={"Authorization":"Bearer {0}".format(auth_token)}).body['data']
    def getTeam(self, name):
        self.team_url = join('http://', self.url, 'teams', name)
        return SunshineTeam(self.team_url)
    def getForumPost(self, post_id, *page_nums):
        post_urls = []
        if len(page_nums) == 1 and page_nums[0] == 'all':
            print unirest.get(join('http://', self.url, 'forums', 'topics', post_id)).body
            num_of_pages, return_code = unirest.get(join('http://', self.url, 'forums', 'topics', post_id)).body['links']['pagination']['last'], \
                                        unirest.get(join('http://', self.url, 'forums', 'topics', post_id)).code
            if not str(return_code).startswith('2'):
                raise sunshineexceptions.SunshineError(return_code)
            for i in range(num_of_pages):
                i += 1
                post_urls.append(join('http://', self.url, 'forums', 'topics', str(post_id + '?page={0}'.format(str(i)))))
        elif len(page_nums) == 1:
            if isinstance(page_nums[0], int):
                post_urls.append(join('http://', self.url, 'forums', 'topics', str(post_id + '?page={0}'.format(page_nums[0]))))
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
                        post_urls.append(join('http://', self.url, 'forums', 'topics', str(post_id + '?page={0}'.format(i))))
                elif page_nums[0].isdigit():
                    post_urls.append(join('http://', self.url, 'forums' 'topics', str(post_id + '?page={0}'.format(page_nums[0]))))
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
                post_urls.append(join('http://', self.url, 'forums', 'topics', str(post_id + '?page={0}'.format(str(item)))))
        elif not page_nums:
            post_urls.append(join('http://', self.url, 'forums', 'topics', str(post_id + '?page=1')))
        print post_urls
        return SunshineTopic(post_urls)
