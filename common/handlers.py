# -*- coding: utf-8 -*-


from tornado import gen
from base.handlers import BaseRequestHandler

__author__ = 'oks'


class HomeHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self):
        # self.render(u'index.html')
        self.render(u'index.html')


class NotFoundHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self):
        self.render(u'404.html')


class LoginHandler(BaseRequestHandler):

    @gen.coroutine
    def post(self):
        self.set_secure_cookie(u"scientist", self.get_argument("name"))

        self.finish()


# class LoginHandler():
#     def post(self):
#         self.set_secure_cookie(u'scientist', self.get_argument(u'name'))
#         self.finish()