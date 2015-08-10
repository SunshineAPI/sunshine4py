#!/usr/bin/env python

from os.path import join
import json
import urllib
import socket
from Players.player import SunshinePlayer
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
    def getPlayer(self, name):
        player_url = join('{0}:{1}'.format(self.server, self.port), 'players', name)
        return SunshinePlayer(name, player_url)
