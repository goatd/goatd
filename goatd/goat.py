import logging
import math
import threading
import time

log = logging.getLogger(__name__)


class Goat(object):
    '''The goat itself. Most of the work is done by the active driver'''
    def __init__(self, driver):
        self.driver = driver
        self.active = False

        self._cached_heading = 0
        self._cached_wind_speed = 0
        self._cached_wind_direction = 0
        self._cached_position = (0, 0)
        self._cached_rudder_position = 0
        self._cached_sail_position = 0

        # wind sensor averaging values (see the paper 'Technologies for
        # Autonomous Sailing: Wings and Wind Sensors')
        self.s = 0  # average sine value
        self.c = 0  # average cosine value
        self.r = 250  # rate of change

        self._update_thread = threading.Thread(target=self.update_cached_values)
        self._update_thread.start()

    def update_cached_values(self):
        '''Run in background and periodically update sensor values.'''
        while True:
            try:
                self._cached_heading = self.driver.heading()
                self._cached_wind_speed = self.driver.wind_speed()
                self._cached_wind_direction = \
                    self._get_wind_average(self.driver.wind_direction())
                self._cached_position = self.driver.position()
            except Exception as e:
                log.error('Got error when trying to update sensor values: '
                          '{}'.format(e))
            time.sleep(0.2)

    def __getattr__(self, name):
        '''Return the requested attribute from the currently loaded driver'''
        return self.driver.handlers.get(name)

    def heading(self):
        return self._cached_heading

    def wind_speed(self):
        return self._cached_wind_speed

    def wind_direction(self):
        return self._cached_wind_direction

    def position(self):
        return self._cached_position

    def rudder(self, angle):
        log.debug('setting rudder angle to {}'.format(angle))
        return self.driver.rudder(angle)

    def sail(self, angle):
        log.debug('setting sail angle to {}'.format(angle))
        return self.driver.sail(angle)

    def _get_wind_average(self, wind_direction):
        self.s += (math.sin(math.radians(wind_direction)) - self.s) / self.r
        self.c += (math.cos(math.radians(wind_direction)) - self.c) / self.r
        a = int(math.degrees(math.atan2(self.s, self.c)))
        if a < 0:
            return a + 360
        else:
            return a
