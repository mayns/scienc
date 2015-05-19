# -*- coding: utf-8 -*-

from benchmarks import handlers_sync

__author__ = 'mayns'

url_handlers = [
    (r"/api/projects(?P<title>[\w+\s+\W+\.\-]+)?$", handlers_sync.ProjectsHandler),
    (r"/api/user", handlers_sync.UserHandler),
]