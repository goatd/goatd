import goatd
import os

class TestConfig(object):
    def test_yaml(self):
        print(__file__)
        self.config = goatd.Config.from_yaml('config.yaml')
        assert self.config.goatd.port == 2222
        
