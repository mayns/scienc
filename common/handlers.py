# -*- coding: utf-8 -*-

import simplejson as json
from tornado import gen
from base.handlers import BaseRequestHandler
import environment

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
        data = json.loads(self.get_argument(u'data', u'{}'))
        email = data.get(u'email', u'')
        pwd = data.get(u'pwd', u'')
        scientist_id = yield ScientistBL.check_scientist(email, pwd)
        if not scientist_id:
            self.send_error(status_code=403)
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


class UserHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self):
        print 'user handler'
        scientist = yield self.get_current_user()
        if not scientist:
            return
        image_url = scientist.image_url and environment.GET_IMG(scientist.image_url, environment.IMG_S)
        scientist_data = dict(
            id=scientist.id,
            image_url=image_url
        )
        response = yield self.get_response(scientist_data)
        self.finish(response)


class CSRFHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self):
        self.prepare()