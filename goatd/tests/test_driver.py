import os
import unittest

import goatd


class TestDriver(unittest.TestCase):
    def setUp(self):
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

    def test_heading(self):
        driver = goatd.load_driver(self.mock_config)
        heading = driver.heading
        assert heading() == 2.43

    def test_wind_speed(self):
        driver = goatd.load_driver(self.mock_config)
        heading = driver.wind_speed
        assert heading() == 25

    def test_empty_hardware(self):
        driver = goatd.load_driver(self.mock_config)
        assert len(driver.some_hardware) == 0

    def test_bad_driver(self):
        self.mock_config.scripts.driver = os.path.join(self.directory,
                                                       'bad_driver.py')
        try:
            driver = goatd.load_driver(self.mock_config)
        except SyntaxError:
            pass
        except Exception as e:
            assert False, 'An exception other than SyntaxError was raised: {}'.format(e)
        else:
            assert False, 'No exception was raised'
