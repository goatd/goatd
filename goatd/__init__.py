from __future__ import print_function

import argparse
import logging
import imp
import os
import sys

from . import logger
from . import plugin
from . import nmea  # noqa
from .api import GoatdHTTPServer, GoatdRequestHandler
from .behaviour import Behaviour
from .behaviour import BehaviourManager
from .goat import Goat
from .color import color
from .config import Config
from .waypoints import WaypointManager
from .driver import BaseGoatdDriver  # noqa
from .base_plugin import BasePlugin  # noqa


__version__ = '2.0.0'

log = logging.getLogger()


def load_conf(conf_file):
    '''
    Return the configuration object. Reads from the first argument by default,
    otherwise falls back to 'goatd-config.yaml'.
    '''

    _, ext = os.path.splitext(conf_file)
    if ext == '.json':
        conf = Config.from_json(conf_file)
    else:
        conf = Config.from_yaml(conf_file)

    conf.filename = conf_file

    return conf


def load_driver(conf):
    '''
    Return the driver module from the filename specified in the configuration
    file with key configuration.scripts.driver.
    '''

    driver_file = conf.driver.get('file', None)
    driver_module_name = conf.driver.get('module', None)

    if driver_file and driver_module_name:
        log.error('you should only specify one of file and module for driver '
                  'configuration')
        exit(1)

    if driver_module_name is not None:
        driver_module = __import__(driver_module_name)
        return driver_module.driver

    expanded_path = os.path.expanduser(conf.driver.file)
    directory, name = os.path.split(expanded_path)
    sys.path.append(os.path.dirname(directory))

    if hasattr(conf, 'filename'):
        conf_directory, _ = os.path.split(conf.filename)
        search_dirs = [directory, conf_directory]
    else:
        search_dirs = [directory]

    module_name = os.path.splitext(name)[0]
    try:
        found_module = imp.find_module(module_name, search_dirs)

        _, filename, _ = found_module
        log.info('Loading goat driver from {}'.format(color(filename, 37)))

        driver_module = imp.load_module('driver_module', *found_module)
        log.info('Using \'{}\' as goat driver'.format(
            color(type(driver_module.driver).__name__, 33)))

    except Exception:
        log.exception('Exception raised in goat driver module')
        raise
    finally:
        found_module[0].close()

    if not isinstance(driver_module.driver, BaseGoatdDriver):
        log.error('Driver module does not instantiate BaseGoatdDriver')
        sys.exit(1)

    return driver_module.driver


def load_behaviours(conf):
    behaviour_manager = BehaviourManager()

    for behaviour in conf.behaviours:
        name = list(behaviour.keys())[0]
        behaviour_conf = behaviour.get(name)
        filename = behaviour_conf.get('file')

        b = Behaviour(name, filename)
        behaviour_manager.add(b)

    return behaviour_manager


def parse_args():
    description = '''\
Experimental robotic sailing goat daemon.
'''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('config', metavar='CONFIG FILE',
                        default='/etc/goatd-config.yaml',
                        nargs='?',
                        help='a path to a configuration file')
    parser.add_argument('--version',
                        action='version',
                        version='goatd {}'.format(__version__))
    return parser.parse_args()


def run():
    '''Run the main server.'''

    args = parse_args()

    conf = load_conf(args.config)

    logger.setup_logging()

    driver = load_driver(conf)
    goat = Goat(driver)

    behaviour_manager = load_behaviours(conf)

    waypoints_file = conf.get('waypoint_file', None)
    waypoints = []
    if waypoints_file is not None:
        with open(waypoints_file) as f:
            lines = f.readlines()
            for point in lines:
                lat, lon = point.split()
                waypoints.append((float(lat), float(lon)))

    waypoint_manager = WaypointManager()

    plugins = plugin.load_plugins(conf, goat, waypoint_manager)

    httpd = GoatdHTTPServer(goat, behaviour_manager, waypoint_manager,
                            (conf.goatd.interface, conf.goatd.port),
                            GoatdRequestHandler)
    while httpd.running:
        try:
            httpd.handle_request()
        except (KeyboardInterrupt, SystemExit):
            log.info('Quitting and requesting plugins end...')
            behaviour_manager.stop()
            for p in plugins:
                p.running = False
            sys.exit()
