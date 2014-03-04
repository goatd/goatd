from __future__ import print_function

import imp
import os
import sys
import traceback

from .goat import Goat
from .config import Config
from .driver import Driver
from .api import GoatdHTTPServer, GoatdRequestHandler


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
        conf_file = sys.argv[1]
    else:
        conf_file = 'goatd-config.yaml'

    _, ext = os.path.splitext(conf_file)
    if ext == '.yaml':
        conf = Config.from_yaml(conf_file)
    elif ext == '.json':
        conf = Config.from_json(conf_file)

    directory, name = os.path.split(conf.scripts.driver)
    module_name = os.path.splitext(name)[0]
    try:
        found_module = imp.find_module(module_name, [directory])
        driver_module = imp.load_module('driver_module', *found_module)
    except:
        print(traceback.format_exc())
    finally:
        found_module[0].close()

    goat = Goat(driver_module.driver)

    httpd = GoatdHTTPServer(goat, ('', conf.goatd.port), GoatdRequestHandler)
    httpd.serve_forever()
