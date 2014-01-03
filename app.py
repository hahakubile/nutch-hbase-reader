from twisted.application.service import Application
from twisted.application.internet import TimerService, TCPServer
from twisted.python import log
from twisted.web import server, static
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.web.template import flatten
import datetime

import config
from element import WebPage
from util import reverseUrl, getRow

def finish_request(output, request):
    """callback used by all resources to finish a request
    """
    request.finish()

def flattenerror(err, request):
    """errback used by all resource to indicate an error during the flatting
    of the renderer and finish the request
    """
    log.err(err)
    request.finish()

class Root(Resource):
    isLeaf = True

    def __init__(self):
        Resource.__init__(self)

    def render_GET(self, request):
        deferred = flatten(request, WebPage(), request.write)
        deferred.addCallback(finish_request, request)
        # in case of error we don't want the browser to stay stuck
        deferred.addErrback(flattenerror, request)
        return NOT_DONE_YET

    def render_POST(self, request):
        baseurl = request.args['baseurl'][0]
        revurl = reverseUrl(baseurl)
        row = getRow(revurl)
        deferred = flatten(request, WebPage(baseurl, revurl, row), request.write)
        deferred.addCallback(finish_request, request)
        deferred.addErrback(flattenerror, request)
        return NOT_DONE_YET

webservice = TCPServer(config.HTTP_PORT,
                       server.Site(Root()), 
                       interface=config.BIND_ADDRESS)
log.msg(format="Web console available at http://%(bind_address)s:%(http_port)s/",
    bind_address=config.BIND_ADDRESS, http_port=config.HTTP_PORT)
application = Application("MiniFrontend")
webservice.setServiceParent(application)
