import unittest

import goatd

class MockDriver(object):
    def heading(self):
        return 2

class TestGoat(unittest.TestCase):
    def setUp(self):
        self.goat = goatd.Goat(MockDriver())

    def test_get_heading(self):
        assert self.goat.heading() == 2

    def test_active(self):
        assert not self.goat.active
