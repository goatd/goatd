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

        base_name = self.conf.goatd.log.gpx.filename
        self.log_dir, name = os.path.split(base_name)
        if os.path.exists(self.log_dir):
            #make sure the log directory is clean
            shutil.rmtree(self.log_dir)

        self.logger = goatd.logging.GpxLogger(self.goat, base_name)

    def test_mock(self):
        assert self.goat.position() == (1, 1)

    def test_correct_config_file(self):
        assert self.conf.name == 'goatd-test-config'

    def test_dir_created(self):
        assert os.path.exists(self.log_dir)
