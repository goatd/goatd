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

import logging

import json

import tornado.ioloop
import tornado.web

from . import exceptions

# reported api version
VERSION = 1.3

log = logging.getLogger(__name__)


def get_wind_dict(goat):
    try:
        speed = goat.wind_speed()
    except (AttributeError, TypeError):
        speed = -1

    try:
        return {'apparent': goat.wind_apparent(),
                'absolute': goat.wind_absolute(),
                'speed': speed}
    except AttributeError:
        log.exception('Error when attempting to read wind direction')
        raise


class GoatdHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'goatd': {'version': VERSION}}
        self.write(response)

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        response = {}
        if data.get('quit'):
            # FIXME: doesn't actually quit the server
            self.running = False
            response['quit'] = True

        self.write(response)


class GoatHandler(tornado.web.RequestHandler):
    def initialize(self, goat):
        self.goat = goat

    def get(self):
        response = {
            'heading': self.goat.heading(),
            'wind': get_wind_dict(self.goat),
            'position': self.goat.position(),
            'active': self.goat.active,
            'rudder_angle': self.goat.target_rudder_angle,
            'sail_angle': self.goat.target_sail_angle,
        }
        self.write(response)


class RudderHandler(tornado.web.RequestHandler):
    def initialize(self, goat):
        self.goat = goat

    def get(self):
        response = {'value': self.goat.target_rudder_angle}
        self.write(response)

    def post(self):
        data = tornado.escape.json_decode(self.request.body)

        value = data.get('value')
        if value:
            self.goat.rudder(value)

        self.write({'value': value})


class SailHandler(tornado.web.RequestHandler):
    def initialize(self, goat):
        self.goat = goat

    def get(self):
        response = {'value': self.goat.target_sail_angle}
        self.write(response)

    def post(self):
        data = tornado.escape.json_decode(self.request.body)

        value = data.get('value')
        if value:
            self.goat.sail(value)

        self.write({'value': value})


class WindHandler(tornado.web.RequestHandler):
    def initialize(self, goat):
        self.goat = goat

    def get(self):
        response = get_wind_dict(self.goat)
        self.write(response)


class BehaviourHandler(tornado.web.RequestHandler):
    def initialize(self, behaviour_manager):
        self.behaviour_manager = behaviour_manager

    def behaviours(self):
        b = {
                behaviour.name: {
                    'running': behaviour.running,
                    'filename': behaviour.filename
                }
                for behaviour in
                self.behaviour_manager.behaviours
        }

        response = {
            'behaviours': b,
            'active': self.behaviour_manager.active_behaviour
        }
        return response

    def get(self):
        self.write(self.behaviours())

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        if 'active' in data:
            behaviour = data.get('active')
            self.behaviour_manager.stop()
            if behaviour is not None:
                self.behaviour_manager.start_behaviour_by_name(behaviour)

        self.write(self.behaviours())


class WaypointHandler(tornado.web.RequestHandler):
    def initialize(self, waypoint_manager):
        self.waypoint_manager = waypoint_manager

    def waypoints(self):
        return {
            'waypoints': self.waypoint_manager.waypoints,
            'home': self.waypoint_manager.home_position,
            'current': self.waypoint_manager.current,
        }

    def get(self):
        self.write(self.waypoints())

    def post(self):
        data = tornado.escape.json_decode(self.request.body)

        waypoints = data.get('waypoints', None)

        try:
            self.waypoint_manager.add_waypoints(waypoints)
        except exceptions.WaypointMalformedError:
            self.write({'error': 'bad waypoint values'})

        self.write(self.waypoints())


class GoatdAPI(object):
    def __init__(self, goat, behaviour_manager, waypoint_manager,
                 server_address):
        log.info('goatd api listening on %s:%s', *server_address)

        self.goat = goat
        self.behaviour_manager = behaviour_manager
        self.waypoint_manager = waypoint_manager
        self.running = True

        self.app = tornado.web.Application([
            (r'/', GoatdHandler),

            (r'/goat', GoatHandler,
                {'goat': self.goat}),

            (r'/rudder', RudderHandler,
                {'goat': self.goat}),

            (r'/sail', SailHandler,
                {'goat': self.goat}),

            (r'/wind', WindHandler,
                {'goat': self.goat}),

            (r'/behaviours', BehaviourHandler,
                {'behaviour_manager': self.behaviour_manager}),

            (r'/waypoints', WaypointHandler,
                {'waypoint_manager': self.waypoint_manager}),
        ])

    def run(self):
        self.app.listen(2222)
        tornado.ioloop.IOLoop.instance().start()
