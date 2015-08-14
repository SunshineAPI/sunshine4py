#!/usr/bin/env python

class BaseSunshineException(Exception):
    """Base sunshine exception class."""
    pass
class Redirection(BaseSunshineException):
    """Raised for 3xx codes."""

class SunshineClientError(BaseSunshineException):
    """Raised for 4xx codes."""

class SunshineServerError(BaseSunshineException):
    """Raised for 5xx codes."""

class SunshineError(BaseSunshineException):
    def __init__(self, code):
        self.code = str(code)
        if self.code.startswith('3'):
            raise Redirection(code)
        elif self.code.startswith('4'):
            raise SunshineClientError(code)
        elif self.code.startswith('5'):
            raise SunshineServerError(code)
