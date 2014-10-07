# -*- coding: utf-8 -*-

from tornado import web
import logging
import sys

__author__ = 'oks'


class BaseRequestHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.payload = dict()
        super(BaseRequestHandler, self).__init__(*args, **kwargs)

    def get_current_user(self):
        return self.get_secure_cookie(u"scientist")

    def post(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def get_payload(self):
        # must be implemented in child class
        raise NotImplementedError


class LoginHandler(BaseRequestHandler):
    def post(self):
        self.set_secure_cookie(u'scientist', self.get_argument(u'name'))
        self.finish()