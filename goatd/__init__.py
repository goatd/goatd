from __future__ import print_function

import imp
import sys
import os
from functools import wraps

from .decorators import *
from .goat import Goat

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
    assert len(sys.argv) > 2
    driver_path = sys.argv[1]

    goatd = imp.new_module('goatd')
    vars(goatd).update(globals())
    driver = Driver(driver_path, goatd)

    behaviour_path = sys.argv[2]

    behaviour = inject_import('behaviour',
                              behaviour_path,
                              {'goat': Goat(driver)})
