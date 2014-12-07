# -*- coding: utf-8 -*-

from urls import url_handlers

from tornado import httpserver, ioloop, web
from tornado.options import define, options
import settings

__author__ = 'oks'

define("port", default=6600, help="run on the given port", type=int)


class ScienceApplication(web.Application):
    def __init__(self, xsrf_cookies=True):
        handlers = url_handlers
        settings_app = dict(
            debug=True,
            xsrf_cookies=xsrf_cookies,
            cookie_secret=settings.COOKIE_SECRET,
            login_url=u"/login",
        )
        web.Application.__init__(self, handlers, **settings_app)


if __name__ == "__main__":
    options.parse_command_line()
    _ioLoop = ioloop.IOLoop.current()

    application = ScienceApplication()

    http_server = httpserver.HTTPServer(application)
    http_server.listen(options.port)

    _ioLoop.start()