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


class GoatdHTTPServer(HTTPServer):
    def __init__(self, goat,
                 server_address, RequestHandlerClass, bind_and_activate=True):

        HTTPServer.__init__(self, server_address, RequestHandlerClass,
                            bind_and_activate)
        self.goat = goat

        self.handles = {
            '/': self.goatd_info,
            '/heading': self.goat_heading
        }

    def goat_heading(self):
        return {'heading': self.goat.heading()}

    def goatd_info(self):
        return {'goatd': {'version': 0.1}}

    def goat_function(self, function_string):
        '''Return the encoded json response from an endpoint string.'''
        json_content = self.handles.get(function_string)()
        return json.dumps(json_content).encode()

    def driver_function(self, function_string):
        obj_path = [p for p in function_string.split('/') if p]
        json_content = {"result": get_deep_attr(self.goat, obj_path)()}
        return json.dumps(json_content).encode()


class GoatdRequestHandler(BaseHTTPRequestHandler):
    server_version = 'goatd/0.1'

    def send_json(self, content):
        self.send_response(200)
        self.send_header('Content-Type', 'application/JSON')
        self.end_headers()
        self.request.sendall(content)

    def do_GET(self, *args, **kwargs):
        '''Handle a GET request to the server'''
        if self.path in self.server.handles:
            self.send_json(self.server.goat_function(self.path))
        else:
            self.send_json((self.server.driver_function(self.path)))

    def do_POST(self):
        '''Handle a POST request to the server'''
        length = int(self.headers.getheader('content-length'))
        data = json.loads(self.rfile.read(length))
        print(data)

    def log_request(self, code='-', size='-'):
        logging.log('REST request {}'.format(self.path), level=logging.VERBOSE)

if __name__ == '__main__':
    class GoatMock(object):
        def __init__(self):
            self.heading = 24.23

    httpd = GoatdHTTPServer(GoatMock(), ('', 2222),
                            GoatdRequestHandler)
    httpd.serve_forever()
