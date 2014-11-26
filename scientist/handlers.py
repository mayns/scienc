# -*- coding: utf-8 -*-

import json
import urllib
import hashlib
from tornado import httpclient, httputil
from tornado import gen, web
from base.handlers import BaseRequestHandler
from scientist.scientist_bl import ScientistBL

__author__ = 'oks'


class ScientistsListHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self):
        print u'scientists list get'
        scientists = yield ScientistBL.get_all_scientists()
        if scientists is None:
            scientists = json.dumps({u'scientists': []})
        self.finish(scientists)


class ScientistHandler(BaseRequestHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        print u'scientist post'
        scientist_dict = json.loads(self.get_argument(u'data', u'{}'))
        scientist_id = yield ScientistBL.add_scientist(scientist_dict)
        response = dict(id=str(scientist_id))
        response_data = yield self.get_response(response)
        self.set_secure_cookie(u'scientist', str(scientist_id))
        self.finish(response_data)

    @gen.coroutine
    def put(self):
        print u'scientist put'
        scientist_dict = json.loads(self.get_argument(u'data', u'{}'))
        yield ScientistBL.update_scientist(scientist_dict[u'scientist'])
        response_data = yield self.get_response(dict())
        self.finish(response_data)

    @gen.coroutine
    @web.authenticated
    def get(self, scientist_id):
        print u'scientist get'
        print self.current_user, type(self.current_user)
        if not self.current_user:
            print u'redirect'
            self.redirect(u'/api/login')
        response = yield ScientistBL.get_scientist(scientist_id)
        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def delete(self, scientist_id):
        print u'scientist delete'
        yield ScientistBL.delete_scientist(scientist_id)
        response_data = yield self.get_response(dict())
        self.finish(response_data)
