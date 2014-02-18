from __future__ import print_function

import imp
import os
import sys

from .goat import Goat
from .config import Config
from .driver import Driver


def inject_import(name, filename, inject):
    module = imp.new_module(name)
    vars(module).update(inject)
    with open(filename) as f:
        exec(f.read(), vars(module))
    return module


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
        conf = Config.from_yaml(sys.argv[1])
    else:
        conf = Config.from_yaml('goatd-config.yaml')

    directory, name = os.path.split(conf.driver)
    module_name = os.path.splitext(name)[0]
    try:
        found_module = imp.find_module(module_name, [directory])
        driver_module = imp.load_module('driver_module', *found_module)
    except Exception, e:
        print(e)
    finally:
        found_module[0].close()

    goat = Goat()

    behaviour = Behaviour(conf.behaviour, goat)
    behaviour.run()
