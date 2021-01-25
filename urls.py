from code.views import MainHandler, UrlHandler, PageHandler, DetailHandler
from settings import settings
import tornado.web


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/page", PageHandler),
        (r"/detail", DetailHandler),
        (r"/(.+)$", UrlHandler),
    ], **settings)
