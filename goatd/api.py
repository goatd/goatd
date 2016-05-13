import logging

from six.moves.BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from six.moves.socketserver import ThreadingMixIn

import json

# reported api version
VERSION = 1.2

log = logging.getLogger(__name__)


def get_deep_attr(obj, path):
    if len(path) > 1:
        attr, path = path[0], path[1:]
        return get_deep_attr(getattr(obj, attr), path)
    else:
        return getattr(obj, path[0])


class GoatdHTTPServer(ThreadingMixIn, HTTPServer):
    '''
    The main REST server for goatd. Listens for requests on port server_address
    and handles each request with RequestHandlerClass.
    '''
    def __init__(self, goat, behaviour_manager,
                 server_address, RequestHandlerClass, bind_and_activate=True):

        HTTPServer.__init__(self, server_address, RequestHandlerClass,
                            bind_and_activate)
        log.info('goatd api listening on %s:%s', *server_address)

        self.goat = goat
        self.behaviour_manager = behaviour_manager
        self.running = True

        # set API endpoints for GETs
        self.handles = {
            '/': self.goatd_info,
            '/goat': self.goat_attr,
            '/wind': self.wind,
            '/active': self.goat_active,
            '/behaviours': self.behaviours,
        }

        # set API endpoints for POSTs
        self.post_handles = {
            '/': self.goatd_post,
            '/behaviours': self.behaviours_post,
        }

    def behaviours(self):
        b = {
                behaviour.name: {
                    'running': behaviour.running,
                    'filename': behaviour.filename
                }
                for behaviour in
                self.behaviour_manager.behaviours
        }

        return {
            'behaviours': b,
            'current': self.behaviour_manager.active_behaviour
        }

    def behaviours_post(self, content):
        if 'current' in content:
            behaviour = content.get('current')
            self.behaviour_manager.stop()
            if behaviour is not None:
                self.behaviour_manager.start_behaviour_by_name(behaviour)

        return self.behaviours()

    def wind(self):
        try:
            speed = self.goat.wind_speed()
        except (AttributeError, TypeError):
            speed = -1

        try:
            return {'direction': self.goat.wind_direction(),
                    'speed': speed}
        except AttributeError:
            log.exception('Error when attempting to read wind direction')
            raise

    def goat_active(self):
        return {'value': self.goat.active}

    def goatd_info(self):
        return {'goatd': {'version': VERSION}}

    def goat_attr(self):
        return {
            'heading': self.goat.heading(),
            'wind': self.wind(),
            'position': self.goat.position(),
            'active': self.goat.active
        }

    def goatd_post(self, content):
        # posting only supports shutting down the server and quitting goatd
        response = {}
        if 'quit' in content:
            if content.get('quit'):
                self.running = False
                response['quit'] = True

        return response

    def goat_post_function(self, name, content):
        f = self.post_handles.get(name)
        if f is not None:
            return f(content)
        else:
            return self.driver_function(name, args=[content['value']])

    def goat_function(self, function_string):
        '''Return the encoded json response from an endpoint string.'''
        json_content = self.handles.get(function_string)()
        return json_content

    def driver_function(self, function_string, args=None):
        '''
        Return the json response from the string describing the path to the
        attribute.
        '''
        if args is None:
            args = []

        obj_path = [p for p in function_string.split('/') if p]
        attr = get_deep_attr(self.goat, obj_path)
        if callable(attr):
            json_content = {"result": attr(*args)}
        else:
            raise AttributeError
        return json_content


class GoatdRequestHandler(BaseHTTPRequestHandler):
    '''
    Handle a single HTTP request. Returns JSON content using data from the rest
    of goatd.
    '''
    server_version = 'goatd/{}'.format(VERSION)

    def send_json(self, content, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/JSON')
        self.end_headers()
        self.request.sendall(content.encode())

    def do_GET(self, *args, **kwargs):
        '''Handle a GET request to the server.'''
        if self.path in self.server.handles:
            # get the function that self.server.handles maps to this path
            handler_func = self.server.goat_function
        else:
            # try handling by poking the driver with a stick
            handler_func = self.server.driver_function

        try:
            func_response = handler_func(self.path)
            code = 200
        except AttributeError:
            log.exception('could not find attribute')
            func_response = "404 - attribute not found"
            code = 404

        if func_response is not None:
            self.send_json(json.dumps(func_response), code)
        else:
            # if the handler runs, but doesn't return anything, 404
            self.send_json("404", code)

    def do_POST(self):
        '''Handle a POST request to the server.'''
        length = int(self.headers.get('content-length'))
        post_body = self.rfile.read(length).decode('utf-8')
        try:
            data = json.loads(post_body)
        except ValueError:
            log.error('Can\'t decode {}'.format(post_body))
            self.send_json("400 - bad json syntax", 400)
        else:
            response_data = self.server.goat_post_function(self.path, data)
            self.send_json(json.dumps(response_data))

    def log_request(self, code='-', size='-'):
        '''Log the request stdout.'''
        log.debug('{} requested'.format(self.path))
