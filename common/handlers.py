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
        from scientist.scientist_bl import ScientistBL
        email = self.get_argument(u'email')
        passw = self.get_argument(u'password')
        scientist_id = yield gen.Task(ScientistBL.check_user_exist, email)
        self.set_secure_cookie(str(scientist_id), hash(scientist_id))
        self.redirect(self.get_argument(u'next', u'/'))


class LogoutHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        scientist_id = self.get_argument(u'scientist_id')
        self.clear_cookie(str(scientist_id))
        self.redirect(self.get_argument(u'next', u'/'))