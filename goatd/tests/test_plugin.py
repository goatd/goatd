import os

import goatd

d, _ = os.path.split(__file__)
PLUGIN_DIR = os.path.join(d, 'plugin')
PLUGIN_FILENAME = os.path.join(PLUGIN_DIR, 'small_plugin.py')

def test_find_plugins():
    plugins = goatd.plugin.find_plugins([PLUGIN_DIR])
    path_in = ['goatd/goatd/tests/plugin/small_plugin.py' in p for p in plugins]
    assert True in path_in

def test_get_module_name():
    assert goatd.plugin.get_module_name(PLUGIN_FILENAME) == 'small_plugin'

def test_load_plugins():
    modules = goatd.plugin.load_plugins(PLUGIN_FILENAME)
    assert True in [hasattr(module, 'THING') for module in modules]

def test_start_plugins():
    class c(object):
        accessed = False
    goat = c()
    modules = goatd.plugin.load_plugins(PLUGIN_FILENAME)
    goatd.plugin.start_plugins(modules, [goat])
    assert goat.accessed == True
