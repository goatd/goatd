import goatd
import os

class TestConfig(object):
    def setup(self):
        self.directory, _ = os.path.split(__file__)
        self.yaml_file = os.path.join(self.directory, 'config.yaml')
        self.json_file = os.path.join(self.directory, 'config.json')

    def test_load_yaml(self):
        config = goatd.Config.from_yaml(self.yaml_file)
        assert config.goatd

    def test_load_json(self):
        config = goatd.Config.from_json(self.json_file)
        assert config.goatd

    def test_port(self):
        config = goatd.Config.from_yaml(self.yaml_file)
        assert config.goatd.port == 2222

    def test_driver(self):
        config = goatd.Config.from_yaml(self.yaml_file)
        assert config.scripts.driver == 'driver.py'

    def test_set_attr(self):
        config = goatd.Config.from_yaml(self.yaml_file)
        config.scripts.driver = 'new_driver.py'
        assert config.scripts.driver == 'new_driver.py'
