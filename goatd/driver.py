from abc import ABCMeta, abstractmethod
import logging
import threading
from functools import wraps

from .color import color

log = logging.getLogger(__name__)


class BaseGoatdDriver(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def heading(self):
        '''
        Must return the heading of the goat in degrees, relative to the world.

        :rtype: float between 0 and 360
        '''
        pass

    @abstractmethod
    def wind_speed(self):
        '''
        Must return the speed the wind is blowing in knots.

        :rtype: float
        '''
        pass

    @abstractmethod
    def wind_direction(self):
        '''
        Must return the direction the wind is blowing in degrees, relative to
        the world.

        :rtype: float between 0 and 360
        '''
        pass

    @abstractmethod
    def position(self):
        '''
        Must return a tuple containing the current latitude and longitude of
        the goat, in that order.

        :rtype: tuple of two floats - ``(float, float)``
        '''
        pass

    @abstractmethod
    def rudder(self, angle):
        '''
        Set the goat's rudder to ``angle`` degrees relative to the goat.

        :param angle: target number of degrees
        :type angle: float between -90 and 90
        '''
        pass

    @abstractmethod
    def sail(self, angle):
        '''
        Set the sail to ``angle`` degrees relative to the goat.

        :param angle: target number of degrees
        :type angle: float between -90 and 90
        '''
        pass
