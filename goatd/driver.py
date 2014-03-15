from functools import wraps

from . import logging
from .color import color


class Driver(object):
    def __init__(self):
        logging.log('Initialising driver')

        self.heading = self.handler('heading')
        self.wind = self.handler('wind')
        self.position = self.handler('position')
        self.rudder = self.handler('rudder')
        self.sail = self.handler('sail')

        self.handlers = {}

    def handler(self, name):
        def wrapper(f):
            @wraps(f)
            def dec(*args, **kwargs):
                return f(*args, **kwargs)
            self.handlers[name] = dec
            logging.log('loaded function {} as {}'.format(
                        color(f.__name__, 32),
                        color('"{}"'.format(name), 35)))
            return dec
        return wrapper