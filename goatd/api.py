try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class GoatdRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        super(GoatdRequestHandler, self).__init__(*args, **kwargs)

    def do_GET(self, *args, **kwargs):
        print('Requested', self.path)
        self.send_response(200)
        self.send_header('Content-Type', 'application/JSON')
        self.end_headers()
        self.request.sendall('hi there'.encode())

if __name__ == '__main__':
    httpd = HTTPServer(('', 2222),
        GoatdRequestHandler)
    httpd.serve_forever()
