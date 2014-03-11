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

    def test_pony_exists(self):
        driver = goatd.load_driver(self.mock_config)
        assert driver.handlers.get('pony')

    def test_pony_runs(self):
        driver = goatd.load_driver(self.mock_config)
        pony = driver.handlers.get('pony')
        assert pony() == 'magic'

    def test_heading(self):
        driver = goatd.load_driver(self.mock_config)
        heading = driver.handlers.get('heading')
        assert heading() == 2.43

    def test_handler_decorators(self):
        driver = goatd.load_driver(self.mock_config)

        @driver.handler('test_handler_decorators')
        def test():
            return 'test passed'

        func = driver.handlers.get('test_handler_decorators')
        assert func() == 'test passed'
