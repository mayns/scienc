# -*- coding: utf-8 -*-

from tornado import web, gen
from common.decorators import base_request

__author__ = 'oks'


class BaseRequestHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.payload = dict()
        super(BaseRequestHandler, self).__init__(*args, **kwargs)

    def get_current_user(self):
        return self.get_secure_cookie(u"scientist")

    @gen.coroutine
    @base_request
    def post(self, *args, **kwargs):
        data = yield self.get_payload()
        self.finish(data)

    @gen.coroutine
    @base_request
    def get(self, *args, **kwargs):
        data = yield self.get_payload()
        self.finish(data)

    @gen.coroutine
    @base_request
    def put(self, *args, **kwargs):
        data = yield self.get_payload()
        self.finish(data)

    @gen.coroutine
    @base_request
    def delete(self, *args, **kwargs):
        data = yield self.get_payload()
        self.finish(data)

    def get_payload(self):
        # must be implemented in child class
        raise NotImplementedError


class LoginHandler(BaseRequestHandler):
    def post(self):
        self.set_secure_cookie(u'scientist', self.get_argument(u'name'))
        self.finish()