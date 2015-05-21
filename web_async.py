# -*- coding: utf-8 -*-

from tornado.ioloop import IOLoop
from tornado.web import Application

from benchmarks.urls_async import url_handlers

from tornado import httpserver
from tornado.options import define, options
import settings
import momoko

__author__ = 'mayns'

define("port", default=6600, help="Science app test: async", type=int)


class AsyncApplication(Application):
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

    application = AsyncApplication()
    _ioLoop = IOLoop.instance()

    application.db = momoko.Pool(
        dsn=u'dbname={database} user={user} password={password} host={host} '
            u'port={port}'.format(**settings.SCIENCE_DB_TEST_MAP[u'NO_SHARD_A']),
        size=1,
        ioloop=_ioLoop,
    )

    # this is a one way to run ioloop in sync
    future = application.db.connect()
    _ioLoop.add_future(future, lambda f: _ioLoop.stop())
    _ioLoop.start()

    http_server = httpserver.HTTPServer(application)
    http_server.listen(options.port)

    _ioLoop.start()