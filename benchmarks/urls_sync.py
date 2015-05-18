# -*- coding: utf-8 -*-

from benchmarks import handlers_sync

__author__ = 'mayns'

url_handlers = [
    (r"/api/projects(/\w+)?", handlers_sync.ProjectsHandler),
]