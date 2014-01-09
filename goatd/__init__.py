from __future__ import print_function

import imp
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

def main():
    conf = Config.from_file('goatd-config.json')

    goatd = imp.new_module('goatd')
    vars(goatd).update(globals())
    driver = Driver(conf.driver, goatd)

    behaviour = inject_import('behaviour',
                              conf.behaviour,
                              {'goat': Goat(driver)})
