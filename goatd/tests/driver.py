import goatd

class TestDriver(goatd.BaseGoatdDriver):
    def __init__(self):
        self.some_hardware = {}

    def reconnect(self):
        pass

    def heading(self):
        return 2.43

    def wind_speed(self):
        return 25

    def rudder(self, angle):
        self.some_hardware['rudder'] = angle

    def position(self):
        pass

    def sail(self):
        pass

    def wind_direction(self):
        pass

driver = TestDriver()
