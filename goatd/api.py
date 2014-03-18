try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from . import logging
import json


def get_deep_attr(obj, path):
    if len(path) > 1:
        attr, path = path[0], path[1:]
        return get_deep_attr(getattr(obj, attr), path)
    else:
        return getattr(obj, path[0])


class GoatdHTTPServer(HTTPServer):
    '''
    The main REST server for goatd. Listens for requests on port server_address
    and handles each request with RequestHandlerClass.
    '''
    def __init__(self, goat,
                 server_address, RequestHandlerClass, bind_and_activate=True):

        HTTPServer.__init__(self, server_address, RequestHandlerClass,
                            bind_and_activate)
        self.goat = goat
        self.running = True

        self.handles = {
            '/': self.goatd_info,
            '/goat': self.goat_attr
        }

        self.post_handles = {
            '/': self.goatd_post,
        }

    def goatd_info(self):
        return {'goatd': {'version': 0.1}}

    def goat_attr(self):
        return {
            'heading' self.goat.heading(),
            'wind' self.goat.wind(),
            'position' self.goat.position()
        }

    def goatd_post(self, content):
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
        return json.dumps(json_content)

    def driver_function(self, function_string, args=None):
        '''
        Return the json response from the string describing the path to the
        attribute.
        '''
        if args is None:
            args = []

        obj_path = [p for p in function_string.split('/') if p]
        attr = get_deep_attr(self.goat, obj_path)
        if attr is not None:
            json_content = {"result": attr(*args)}
        else:
            raise AttributeError
        return json.dumps(json_content)


class GoatdRequestHandler(BaseHTTPRequestHandler):
    '''
    Handle a single HTTP request. Returns JSON content using data from the rest
    of goatd.
    '''
    server_version = 'goatd/0.1'

    def send_json(self, content, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/JSON')
        self.end_headers()
        self.request.sendall(content.encode())

    def do_GET(self, *args, **kwargs):
        '''Handle a GET request to the server.'''
        if self.path in self.server.handles:
            handler_func = self.server.goat_function
        else:
            handler_func = self.server.driver_function

        try:
            func_response = handler_func(self.path)
            code = 200
        except AttributeError:
            func_response = "404 - attribute not found"
            code = 404

        if func_response is not None:
            self.send_json(func_response, code)
        else:
            self.send_json("404", code)

    def do_POST(self):
        '''Handle a POST request to the server.'''
        length = int(self.headers.get('content-length'))
        data = json.loads(self.rfile.read(length).decode('utf-8'))
        response_data = self.server.goat_post_function(self.path, data)
        self.send_json(json.dumps(response_data))

    def log_request(self, code='-', size='-'):
        '''Log the request stdout.'''
        logging.log('REST request {}'.format(self.path), level=logging.VERBOSE)
