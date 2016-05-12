import imp
import logging
import os

from .color import color

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
        for directory in search_directories:
            path = os.path.join(directory, plugin_name) + '.py'
            if os.path.isfile(path):
                found_plugins.append(path)

    return found_plugins


def load_plugins(plugin_names):
    modules = []
    for module_filename in plugin_names:
        with open(module_filename) as f:
            module = imp.load_module(
                get_module_name(module_filename),
                f,
                module_filename,
                ('.py', 'U', 1)
            )
            modules.append(module)
            log.info('Loaded plugin from {}'.format(
                     color(module_filename, 37)))

    return modules


def start_plugins(modules, goat):
    for module in modules:
        log.info('Starting plugin from {}'.format(
                 color(module.__file__, 37)))

        goatd = get_goatd_module(goat)
        plugin = module.plugin({}, goatd)
        plugin.start()


def get_plugin_names_from_config(config):
    return [list(plugin.keys())[0] for plugin in config.plugins]
