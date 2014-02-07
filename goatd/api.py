from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

class Root(Resource):
    def render_GET(self, request):
        return 'sup, goat'

class Goatd(Resource):
    def getChild(self, name, request):
        uri = request.uri
        print uri
        return Root()

root = Goatd()
factory = Site(root)
