import os
import shutil

import goatd

class MockGoat(object):
    def __init__(self):
        self.pos = 0

    def position(self):
        self.pos += 1
        return (self.pos, self.pos)

class TestGpxLogging(object):
    def setup(self):
        self.goat = MockGoat()
        self.conf = goatd.Config.from_yaml('goatd-config.yaml')

        log_dir = os.path.dirname(self.conf.goatd.log.gpx.filename)
        if os.path.isdir(log_dir):
            #make sure the log directory is clean
            shutil.rmtree(log_dir)

    def test_mock(self):
        assert self.goat.position() == (1, 1)

    def test_correct_config_file(self):
        assert self.conf.name == 'goatd-test-config'
