import goatd

class TestPlugin(goatd.BasePlugin):
    def __init__(self, conf, goatd):
        self.accessed = False
        self.goat = goatd

    def main(self):
        self.goat.accessed = True

plugin = TestPlugin
