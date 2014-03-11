try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

import logging
import json


def get_deep_attr(obj, path):
    if len(path) > 1:
        attr, path = path[0], path[1:]
        return get_deep_attr(getattr(obj, attr), path)
    else:
        return getattr(obj, path[0])


class BoatdHTTPServer(HTTPServer):
    '''
    The main REST server for boatd. Listens for requests on port server_address
    and handles each request with RequestHandlerClass.
    '''
    def __init__(self, boat,
                 server_address, RequestHandlerClass, bind_and_activate=True):

        HTTPServer.__init__(self, server_address, RequestHandlerClass,
                            bind_and_activate)
        self.boat = boat
        self.running = True

        self.handles = {
            '/': self.boatd_info,
            '/heading': self.boat_heading
        }

        self.post_handles = {
            '/': self.boatd_post,
        }

    def boat_heading(self):
        return {'heading': self.boat.heading()}

    def boatd_info(self):
        return {'boatd': {'version': 0.1}}

    def boatd_post(self, content):
        response = {}
        if 'quit' in content:
            if content.get('quit'):
                self.running = False
                response['quit'] = True

        return response

    def boat_post_function(self, name, content):
        return self.post_handles.get(name)(content)

    def boat_function(self, function_string):
        '''Return the encoded json response from an endpoint string.'''
        json_content = self.handles.get(function_string)()
        return json.dumps(json_content).encode()

    def driver_function(self, function_string):
        '''
        Return the json response from the string describing the path to the
        attribute.
        '''
        obj_path = [p for p in function_string.split('/') if p]
        json_content = {"result": get_deep_attr(self.boat, obj_path)()}
        return json.dumps(json_content).encode()


class BoatdRequestHandler(BaseHTTPRequestHandler):
    '''
    Handle a single HTTP request. Returns JSON content using data from the rest
    of boatd.
    '''
    server_version = 'boatd/0.1'

    def send_json(self, content):
        self.send_response(200)
        self.send_header('Content-Type', 'application/JSON')
        self.end_headers()
        self.request.sendall(content)

    def do_GET(self, *args, **kwargs):
        '''Handle a GET request to the server.'''
        if self.path in self.server.handles:
            self.send_json(self.server.boat_function(self.path))
        else:
            self.send_json((self.server.driver_function(self.path)))

    def do_POST(self):
        '''Handle a POST request to the server.'''
        length = int(self.headers.getheader('content-length'))
        data = json.loads(self.rfile.read(length))
        if self.path in self.server.post_handles:
            response_data = self.server.boat_post_function(self.path, data)
            self.send_json(json.dumps(response_data).encode())

    def log_request(self, code='-', size='-'):
        '''Log the request stdout.'''
        logging.log('REST request {}'.format(self.path), level=logging.VERBOSE)

if __name__ == '__main__':
    class BoatMock(object):
        def __init__(self):
            self.heading = 24.23

    httpd = BoatdHTTPServer(BoatMock(), ('', 2222),
                            BoatdRequestHandler)
    httpd.serve_forever()