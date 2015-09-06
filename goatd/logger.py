from __future__ import print_function

import logging
import os
import time

from .color import color

VERBOSE, NORMAL, WARN, ERROR = range(4)


def log(message, level=NORMAL):
    messages = []
    if level > WARN:
        text = 'WARNING'
        if level == ERROR:
            text = 'ERROR'
        messages.append('[{}]'.format(color(text, 31)))

    messages.append(message)
    print(time.strftime('[%H:%M:%S]'), *messages)

def setup_logging():
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)
    logging.debug('Logging configured')
