import unittest

import goatd

class MockDriver(object):
    def __init__(self):
        self.handlers = {
            'heading': lambda: 2.43,
            'pony': lambda: 'magic'
        }

class TestGoat(unittest.TestCase):
    def setUp(self):
        self.goat = goatd.Goat(MockDriver())

    def test_get_heading(self):
        assert self.goat.heading() == 2.43

    def test_get_pony(self):
        assert self.goat.pony() == 'magic'

    def test_active(self):
        assert not self.goat.active
