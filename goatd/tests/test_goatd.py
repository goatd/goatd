import sys
import os

import goatd

class TestGoatd(object):
    def __init__(self):
        sys.argv = sys.argv[0:1]
        self.directory, _ = os.path.split(__file__)

    def test_load_json_config(self):
        conf_file = os.path.join(self.directory, 'config.json')
        conf = goatd.load_conf(sys.argv + [conf_file])
        assert conf.scripts.driver == 'driver.py'

    def test_load_yaml_config(self):
        conf_file = os.path.join(self.directory, 'config.yaml')
        conf = goatd.load_conf(sys.argv + [conf_file])
        assert conf.scripts.driver == 'driver.py'
