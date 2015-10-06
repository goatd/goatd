import goatd

class TestUtils(object):
    def test_reldir(self):
        assert goatd.utils.reldir('test/thing.py', 'dir') == 'test/dir'
