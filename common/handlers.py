# -*- coding: utf-8 -*-


from tornado import gen
from base.handlers import BaseRequestHandler

__author__ = 'oks'


class HomeHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self):
        self.render(u'index.html')


class NotFoundHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self):
        self.render(u'404.html')


