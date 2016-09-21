import unittest

import goatd

from .driver import TestDriver


class TestGoat(unittest.TestCase):
    def setUp(self):
        self.goat = goatd.Goat(TestDriver())
        self.goat.update_cached_values()

    def test_get_heading(self):
        assert self.goat.heading() == 2.43

    def test_active(self):
        assert not self.goat.active
