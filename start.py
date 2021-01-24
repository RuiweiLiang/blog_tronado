import json, logging

import tornado.ioloop
import tornado.web
from urls import make_app

if __name__ == "__main__":
    app = make_app()
    app.listen(8080, address="0.0.0.0", xheaders=True)
    tornado.ioloop.IOLoop.current().start()
