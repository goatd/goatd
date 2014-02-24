from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class GoatdRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self, *args, **kwargs):
        print('Requested', self.path)

if __name__ == '__main__':
    httpd = HTTPServer(('', 8000),
            GoatdRequestHandler)
    httpd.serve_forever()
