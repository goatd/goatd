import goatd

class MockDriver(object):
    def __init__(self):
        self.handlers = {
            'heading': lambda: 2.43,
            'pony': lambda: 'magic'
        }

class TestGoat(object):
    def setup(self):
        self.goat = goatd.Goat(MockDriver())

    def test_get_heading(self):
        assert self.goat.heading() == 2.43

    def test_get_pony(self):
        assert self.goat.pony() == 'magic'
