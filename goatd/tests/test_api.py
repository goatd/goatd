import threading

import goatd

class MockGoat(object):
    def __init__(self):
        self.heading = 45

class TestAPI(object):
    def setup(self):
        httpd = goatd.GoatdHTTPServer(MockGoat(), ('', 2222),
                    goatd.GoatdRequestHandler)
        self.http_thread = threading.Thread(target=httpd.handle_request)
        self.http_thread.daemon = True
        self.http_thread.start()

    def test_thread(self):
        assert self.http_thread.is_alive()
