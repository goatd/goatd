try:
    from urllib.request import urlopen
    from urllib.request import HTTPError
except ImportError:
    from urllib2 import urlopen
    from urllib2 import HTTPError

import threading
import socket
import json

import goatd


class MockGoat(object):
    def __init__(self):
        self.heading = lambda: 45
        self.pony = lambda: 'magic'


class TestAPI(object):
    TEST_PORTS = 10

    def __init__(self):
        self.port = 2222

    def setup(self):
        for _ in range(self.TEST_PORTS):
            try:
                httpd = goatd.GoatdHTTPServer(MockGoat(), ('', self.port),
                                              goatd.GoatdRequestHandler)
                break
            except socket.error:
                self.port += 1

        self.http_thread = threading.Thread(target=httpd.handle_request)
        self.http_thread.daemon = True
        self.http_thread.start()

    def _base_url(self):
        return 'http://localhost:{}'.format(self.port)

    def _url(self, endpoint):
        return self._base_url() + endpoint

    def test_thread(self):
        assert self.http_thread.is_alive()

    def test_GET(self):
        assert urlopen(self._base_url()).read()

    def test_valid_json(self):
        content = urlopen(self._base_url()).read()
        d = json.loads(content.decode("utf-8"))
        assert 'goatd' in d

    def test_request_pony(self):
        content = urlopen(self._url('/pony')).read()
        d = json.loads(content.decode("utf-8"))
        assert d.get('result') == 'magic'

    def test_request_nested(self):
        content = urlopen(self._url('/nest/thing')).read()
        d = json.loads(content.decode("utf-8"))
        assert d.get('result') == 'well hello there'

    def test_request_nonexistant(self):
        try:
            urlopen(self._url('/does_not_exist'))
            assert '404 code returned' == True
        except HTTPError as e:
            assert e.code == 404

    def test_request_heading(self):
        content = urlopen(self._url('/heading')).read()
        d = json.loads(content.decode("utf-8"))
        assert d.get('heading') == 45

    def test_content_type(self):
        m = urlopen(self._url('/heading')).info()
        assert m['content-type'] == 'application/JSON'

    def test_response_code(self):
        code = urlopen(self._url('/heading')).getcode()
        assert code == 200
