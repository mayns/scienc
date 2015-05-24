# -*- coding: utf-8 -*-

from benchmarks import handlers_sync
from stands import handlers

__author__ = 'mayns'

url_handlers = [
    (r"/api/projects(/\w+)?", handlers_sync.ProjectsHandler),
    (r"/api/user", handlers_sync.UserHandler),
    (r"/api/stand/items", handlers.ServerGenTemplateItemsHandler),
    (r"/api/stand/item(/\w+)?", handlers.ServerGenTemplateItemHandler),
]