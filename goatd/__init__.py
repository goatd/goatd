from __future__ import print_function

import imp
import sys
import os
from functools import wraps

from .decorators import *
from .goat import Goat
from .config import Config

def inject_import(name, filename, inject):
    module = imp.new_module(name)
    vars(module).update(inject)
    with open(filename) as f:
        exec(f.read(), vars(module))
    return module

class Driver(object):
    def __init__(self, driver_path, goatd):
        self.module = inject_import('driver',
                                    driver_path,
                                    {'goatd': goatd})
        self.path = driver_path

class Behaviour(object):
    def __init__(self, behaviour_path, goat):
        self.goat = goat
        self.path = behaviour_path

    def run(self):
        return inject_import('behaviour',
                              self.path,
                              {'goat': self.goat})

def main():
    if len(sys.argv) > 1:
        conf = Config.from_file(sys.argv[1])
    else:
        conf = Config.from_file('goatd-config.json')

    this = imp.new_module('goatd')
    vars(this).update(globals())
    driver = Driver(conf.driver, this)

    behaviour = Behaviour(conf.behaviour, Goat(driver))

    for b in ['example/basic_behaviour.py', 'example/b2.py', 'example/b3.py']:
        behaviour.path = b
        behaviour.run()
