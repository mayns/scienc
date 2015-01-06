# -*- coding: utf-8 -*-

import simplejson as json
from tornado import gen
from base.handlers import BaseRequestHandler

__author__ = 'oks'

# TODO: auth error
# TODO: auth redirect


class NotFoundRedirectHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self):
        self.redirect(u'/api/not-found')


class NotFoundHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        import random
        colors = [u'192430', u'E29611', u'0A926A', u'2F75BE', u'CC2979']
        i = random.randrange(5)
        self.write("<html><div style='color: #{color};font-size: 500px; text-align: center; vertical-align: middle; "
                   "font-family: Helvetica, Arial, Sans-serif'; >42</div></html>".format(color=colors[i]))


class LoginHandler(BaseRequestHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        from scientist.scientist_bl import ScientistBL
        print u'login'
        data = json.loads(self.get_argument(u'data', u'{}'))
        email = data.get(u'email', u'')
        password = data.get(u'password', u'')
        scientist_id = yield ScientistBL.check_scientist(email, password)
        if not scientist_id:
            self.finish(u'LOGIN or PASSWORD NOT CORRECT')
            return
        self.set_secure_cookie(u'scientist', str(scientist_id))
        self.redirect(self.get_argument(u'next', u'/'))

    @gen.coroutine
    def get(self, *args, **kwargs):
        self.redirect(self.get_argument(u'next', u'/'))


class LogoutHandler(BaseRequestHandler):
    def post(self, *args, **kwargs):
        print u'logout'
        scientist_id = self.get_secure_cookie(u'scientist')
        if not scientist_id:
            raise Exception(u'WTF???')
        self.clear_cookie(u'scientist')
        self.redirect(self.get_argument(u'next', u'/'))


class CSRFHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self):
        x = self.xsrf_token
        if not x:
            yield self.xsrf_token()