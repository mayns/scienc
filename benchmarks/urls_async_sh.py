# -*- coding: utf-8 -*-

from benchmarks import handlers_async_sh

__author__ = 'mayns'

url_handlers = [
    (r"/api/projects(/\w+)?", handlers_async_sh.ProjectsHandler),
    (r"/api/user", handlers_async_sh.UserHandler),
]