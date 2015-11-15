import goatd
import unittest

class TestUtils(unittest.TestCase):
    def test_reldir(self):
        assert goatd.utils.reldir('test/thing.py', 'dir') == 'test/dir'
