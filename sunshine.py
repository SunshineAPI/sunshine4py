#!/usr/bin/env python

import os
import json
import urllib
import socket
import Players
try:
    from pip import get_installed_distributions
    packages = get_installed_distributions()
    packages_list = sorted(["%s" % (i.key) for i in packages])
    if 'unirest' in packages_list:
        import unirest
except ImportError as e:
    print 'Cannot import Unirest, either you don\'t have it installed, \n \
           or it isn\'t installed properly. ' + str(e)
except Exception:
    print 'Unexpected exception'

class Sunshine:
    def __init__(self, server, port):
        if not isinstance(server, str):
            raise TypeError("Server address must be str")
        elif not isinstance(port, int):
            if isinstance(port, str):
                try:
                    port = int(port)
                except Exception:
                    raise Exception('port number must be an int or str')
            else:
                raise TypeError('port number must be an int or str')
