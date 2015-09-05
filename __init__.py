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

from sunshine4py import sunshineexceptions
from sunshine4py import Players
from sunshine4py import Teams
from sunshine4py import Stats
from sunshine4py import Tournaments
from sunshine4py import Forums
from sunshine4py.sunshineexceptions import checkCode
from os.path import join
from Teams.teams import SunshineTeams
from Teams.team import SunshineTeam
from Players.player import SunshinePlayer
from Stats.stat import SunshineStats
from Tournaments.tournament import SunshineTournament
from Tournaments.tournaments import SunshineTournamentList
from Forums.forum_topic import SunshineTopic
from Forums.forum_category import SunshineForumCategory
import json
import urllib
import socket

def parsePages(list, form, *page_nums):
    page_nums = page_nums[0]
    if len(page_nums) == 1:
        if isinstance(page_nums[0], int):
            list.append(form.format(page_nums[0]))
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
                    list.append(form.format(i))
            elif page_nums[0].isdigit():
                list.append(form.format(page_nums[0]))
            elif page_nums[0] == 'all':
                num_of_pages, return_code = unirest.get(form.format('')).body['links']['pagination']['last'], \
                                            unirest.get(form.format('')).code
                sunshineexceptions.checkCode(return_code)
                for i in range(num_of_pages):
                    list.append(form.format(i))
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
            list.append(form.format(str(item)))
    return list
class Sunshine:
    """Sunshine class. To create an instance of this class, execute
    sunshine4py.Sunshine(). If you pass in no arguments, it creates
     an instance from your localhost at port 3000. You can pass in
    arguments to create an instance of the Sunshine class from
    A different server. To do this, simply pass in the arguments
    either the IP address of your server, or the domain name.
    ex. sunshine4py.Sunshine('sunshine-api.com', 80)
    (Without the http://.) To find out more, enter the name of
    a function followed by `.__doc__`. The functions in the
    Sunshine class are as follows:
    __init__ : class constructor.
    getPlayer: retrieves player data.
    getTeams : retrieves list of teams.
    getStats : retrieves statistics of players.
    getTournament: gets info on current or past tournament.
    getTournamentList: retreives all tournaments, past or current.
    getAuth  : returns a player's authentication token after inputing
    username and password. (for more information, see issue #49 of the
    WebAPI and AUTHTUTORIAL.MD.)
    getAlerts: gets a player's alerts after inputing auth token.
    getTeam  : gets a specific team.
    getForumTopic: gets a specific topic on the forums.
    getForumCategory: gets an entire forum category."""
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
        """Pass in desired player's name as an argument
        . eg. getPlayer('Apple')"""
        player_url = join(self.url, 'players', name)
        return SunshinePlayer(name, player_url)
    def getTeams(self, *page_nums):
        """Pass in page numbers as an argument. There
        are multiple ways you can do this. Either pass
        in integers separated by a comma, a string
        containing digits separated by a comma, a single
        integer, a string containing a single number, or
        a string containing a range of numbers. eg.
        '1-10' You can retrieve every page by inputting
        'all'"""
        print 'teams args' + str(page_nums)
        teams_urls = []
        parsePages(teams_urls, join('http://', self.url, 'teams', '?page={0}'), page_nums)
        return SunshineTeams(teams_urls)
    def getStats(self, *page_nums):
        """Pass in page numbers as an argument. There
        are multiple ways you can do this. Either pass
        in integers separated by a comma, a string
        containing digits separated by a comma, a single
        integer, a string containing a single number, or
        a string containing a range of numbers. eg.
        '1-10' You can retrieve every page by inputting
        'all'"""
        url_list = []
        parsePages(url_list, join('http://', self.url, 'stats', '?page={0}'), page_nums)
        return SunshineStats(url_list)
    def getTournament(self, name):
        """Pass in the name of desired tournament as
        an arugment. Either enter each word separated
        by a hyphen, or enter it normally, with all
        non-alphabetical characters removed. It will
        automatically be formatted."""
        if name.count(' ') >= 1:
            name = '-'.join(name.split()).lower()
        else:
            name = name.lower()
        url = join('http://', self.url, 'tournaments', name)
        return SunshineTournament(url)
    def getTournamentList(self):
        """No arguments needed. Just call the function
        normally."""
        return SunshineTournamentList(join('http://', self.url, 'tournaments'))
    def getAuth(self, email, password):
        """Enter your email and password for oc.tc.
        If you don't feel comfortable doing this,
        follow the instructions in AUTHTUTORIAL.md
        to get your auth token."""
        self.return_code = unirest.post(join('http://', self.url, 'players', 'auth'),
            headers={"Content-Type":"application/json", "Authorization":"Basic","Accept":"application/json"},
            params=json.dumps({"email":"{0}".format(email),"password":"{0}".format(password)})).code
        checkCode(self.return_code)
        return str(unirest.post(join('http://', self.url, 'players', 'auth'),
            headers={"Content-Type":"application/json", "Authorization":"Basic","Accept":"application/json"},
            params=json.dumps({"email":"{0}".format(email),"password":"{0}".format(password)})).body['token'])
    def getAlerts(self, auth_token):
        """Pass in your auth token, and it will return your alerts."""
        self.return_code = unirest.get(join('http://', self.url, 'alerts'),headers={"Authorization":"Bearer {0}".format(auth_token)}).code
        checkCode(self.return_code)
        return unirest.get(join('http://', self.url, 'alerts'),
                headers={"Authorization":"Bearer {0}".format(auth_token)}).body['data']
    def getTeam(self, name):
        """Enter the team's name as an argument."""
        self.team_url = join('http://', self.url, 'teams', name)
        return SunshineTeam(self.team_url)
    def getForumTopic(self, post_id, *page_nums):
        """Two arguments are needed. The id of the topic, and
        the page numbers. There are multiple ways you
        can do this pass in the page numbers as arguments.
        Either pass in integers separated by a comma, a
        string containing digits separated by a comma,
        a single integer, a string containing a single
        number, or a string containing a range of numbers. eg.
        '1-10' You can retrieve every page by inputting
        'all'"""
        post_urls = []
        parsePages(post_urls, join('http://', self.url, 'forums', 'topics', post_id, '?page={0}'), page_nums)
        return SunshineTopic(post_urls, self.url)
    def getForumCategory(self, cat_id, *page_nums):
        """Two arguments are needed. the id of the category, and
        the page numbers. There are multiple ways you
        can do this pass in the page numbers as arguments.
        Either pass in integers separated by a comma, a
        string containing digits separated by a comma,
        a single integer, a string containing a single
        number, or a string containing a range of numbers. eg.
        '1-10' You can retrieve every page by inputting
        'all'"""
        cat_urls = []
        parsePages(post_urls, join('http://', self.url, 'forums', 'topics', cat_id, '?page={0}'), page_nums)
        return SunshineForumCategory(cat_urls, self.url)
