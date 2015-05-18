# -*- coding: utf-8 -*-

import logging
from tornado import web, gen

__author__ = 'mayns'


class ProjectsHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(ProjectsHandler, self).__init__(*args, **kwargs)
        self.application = None
        self.payload = dict()

    @gen.coroutine
    def get(self):
        logging.info(u'Async GET')
        pass

    @gen.coroutine
    def post(self, *args, **kwargs):
        logging.info(u'Async POST')
        pass