# -*- coding: utf-8 -*-

from tornado.ioloop import IOLoop
from tornado.web import Application

from benchmarks.urls_sync import url_handlers

from tornado import httpserver
from tornado.options import define, options
import settings

__author__ = 'mayns'

define("port", default=6600, help="Science app test: sync", type=int)


class SyncApplication(Application):
    def __init__(self):
        handlers = url_handlers
        settings_app = dict(
            debug=True,
            cookie_secret=settings.COOKIE_SECRET,
            template_path=settings.TEMPLATE_PATH,
            static_path=settings.STATIC_PATH,
        )
        Application.__init__(self, handlers, **settings_app)


if __name__ == "__main__":
    options.parse_command_line()
    _ioLoop = IOLoop.current()

    application = SyncApplication()

    http_server = httpserver.HTTPServer(application)
    http_server.listen(options.port)

    _ioLoop.start()