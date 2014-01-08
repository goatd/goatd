from __future__ import print_function

import imp
import sys
import os
import time
from functools import wraps

class Goat(object):
    def __init__(self):
        pass

    def __getattr__(self, name):
        return lambda *args: print('called:', name)

def module_name(path):
    return os.path.splitext(os.path.split(path)[-1])[0]

def inject_import(filename, inject):
    name = module_name(filename)
    module = imp.new_module(name)
    vars(module).update(inject)
    with open(filename) as f:
        exec(f.read(), vars(module))
    sys.modules[name] = module
    return module

def log(message):
    print(time.strftime('[%H:%M:%S]'), message)

def do_something(func):
    @wraps(func)
    def inner(*args, **kwargs):
        r = func(*args, **kwargs)
        log('did something and got {}'.format(r))
        return r
    return inner

assert len(sys.argv) > 2
goatd = imp.new_module('goatd')
vars(goatd).update(globals())
drive_path = sys.argv[1]
inject_import(drive_path, {'goatd': goatd})

behaviour_path = sys.argv[2]
inject_import(behaviour_path, {'goat': Goat()})
