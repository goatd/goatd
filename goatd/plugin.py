import imp
import logging
import os
import threading

from .color import color
from . import utils
from .config import Config

log = logging.getLogger(__name__)


class Goatd(object):
    def __init__(self, goat):
        self.goat = goat


goatd_module = None


def get_goatd_module(goat):
    global goatd_module
    if goatd_module is None:
        goatd_module = Goatd(goat)

    return goatd_module


def get_module_name(filepath):
    _, name = os.path.split(filepath)
    module_name, _ = os.path.splitext(name)
    return module_name


def find_plugins(search_directories, enabled_plugins):
    found_plugins = []

    for plugin_name in enabled_plugins:
        found = False
        for directory in search_directories:
            path = os.path.join(directory, plugin_name) + '.py'
            if os.path.isfile(path):
                found = True
                found_plugins.append((plugin_name, path))

        if found is not True:
            log.warning('Could not find an appropriate module for plugin '
                        '\'{}\''.format(color(plugin_name, 31)))

    return found_plugins


def start_plugin(module, conf, goat):
    log.info('Starting plugin {} with config \'{}\''.format(
             color(module.plugin.__name__, 37),
             color(str(conf), 36)))

    goatd = get_goatd_module(goat)
    plugin = module.plugin(conf, goatd)

    t = threading.Thread(target=plugin.start)
    t.start()

    return plugin


def load_plugins(conf, goat):
    plugin_dirs = [utils.reldir(__file__, 'coreplugins')]

    if conf.get('plugin_directory') is not None:
        plugin_dirs += [conf.plugin_directory]

    plugin_names = get_plugin_names_from_config(conf)

    found_plugins = find_plugins(plugin_dirs, plugin_names)

    plugins = []
    for (name, module_filename) in found_plugins:
        with open(module_filename) as f:
            module = imp.load_module(
                get_module_name(module_filename),
                f,
                module_filename,
                ('.py', 'U', 1)
            )
            log.info('Loaded plugin from {}'.format(
                     color(module_filename, 37)))

            plugin_conf = get_config_for_plugin(conf, name)
            plugins.append(start_plugin(module, plugin_conf, goat))

    return plugins


def get_plugin_names_from_config(config):
    return [list(plugin.keys())[0] for plugin in config.plugins]


def get_config_for_plugin(config, plugin_name):
    for plugin in config.plugins:
        conf = plugin.get(plugin_name)
        return Config(conf)
