# This file is part of goatd, the Robotic Sailing Goat Daemon.
#
# Copyright (C) 2013-2017 Louis Taylor <louis@kragniz.eu>
#
# goatd is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# goatd is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from goatd import BasePlugin

import datetime
import time


log_format = (
             '{time}, '
             #'bhead={head} '
             #'wind={wind} '
             '{lat}, '
             '{long}, '
             #'nwlat={wpn} '
             #'nwlon={wpe} '
             #'nwn={num} '
             #'spos={sail} '
             #'rpos={rudder} '
             #'whead={waypoint_heading} '
             #'distance={waypoint_distance} '
             #'speed={speed} '
             '\n'
             )


class LoggerPlugin(BasePlugin):
    def main(self):
        period = self.config.period
        filename = self.config.filename

        while self.running:
            heading = self.goatd.goat.heading()
            wind_direction = self.goatd.goat.wind_absolute()
            lat, lon = self.goatd.goat.position()

            ts = time.time()

            log_line = log_format.format(
                    time=time.strftime("%H%M%S%d"),
                    #head=heading,
                    #wind=wind_direction,
                    lat=str(lat*(10**7)).split(".",1)[0],
                    long=str(lon*(10**7)).split(".",1)[0],
            )

            with open(filename, 'a') as f:
                f.write(log_line)

            time.sleep(period)

plugin = LoggerPlugin
