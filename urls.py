from code.views import MainHandler, UrlHandler, PageHandler, DetailHandler,UploadImgHandler,UploadTextHandler
from settings import settings
import tornado.web


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/page", PageHandler),
        (r"/detail", DetailHandler),
        (r"/upload_img", UploadImgHandler),
        (r"/upload_text", UploadTextHandler),
        (r"/(.+)$", UrlHandler),
    ], **settings)
