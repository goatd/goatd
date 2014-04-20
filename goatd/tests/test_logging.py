import goatd

class MockGoat(object):
    def __init__(self):
        self.pos = 0

    def position(self):
        self.pos += 1
        return (self.pos, self.pos)

class TestLogging(object):
    def setup(self):
        self.goat = MockGoat()

    def test_mock(self):
        assert self.goat.position() == (1, 1)
