import os

import goatd


class TestDriver(object):
    def setup(self):
        self.directory, _ = os.path.split(__file__)

        configuration = {
            'scripts': {
                'driver': os.path.join(self.directory, 'driver.py')
            }
        }
        self.mock_config = goatd.Config(configuration)

        self.driver_file = os.path.join(self.directory,
            self.mock_config.scripts.driver)

    def test_driver_file(self):
        assert os.path.isfile(self.driver_file)

    def test_loading_driver(self):
        assert goatd.load_driver(self.mock_config)
