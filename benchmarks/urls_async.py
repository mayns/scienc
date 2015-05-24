# -*- coding: utf-8 -*-

from benchmarks import handlers_async
from stands import handlers

__author__ = 'mayns'

url_handlers = [
    (r"/api/projects(/\w+)?", handlers_async.ProjectsHandler),
    (r"/api/user", handlers_async.UserHandler),
    (r"/api/stand/items", handlers.ServerGenTemplateItemsHandler),
    (r"/api/stand/item(/\w+)?", handlers.ServerGenTemplateItemHandler),
]