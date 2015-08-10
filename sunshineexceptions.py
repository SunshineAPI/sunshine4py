#!/usr/bin/env python

class BaseSunshineException(Exception):
    def __init__(self):
        pass

class PlayerError(BaseSunshineException):
    """Error raised when a user tries to fetch data
    from an invalid player 'ie. player doesn't exist"""
