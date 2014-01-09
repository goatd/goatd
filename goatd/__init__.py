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
    sys.modules[name] = module
    return module

def main():
    assert len(sys.argv) > 2
    goatd = imp.new_module('goatd')
    vars(goatd).update(globals())
    driver_path = sys.argv[1]
    driver = inject_import('driver', driver_path, {'goatd': goatd})

    behaviour_path = sys.argv[2]
    behaviour = inject_import('behaviour',
                              behaviour_path,
                              {'goat': Goat(driver)})
