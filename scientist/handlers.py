# -*- coding: utf-8 -*-

import json
import urllib
import hashlib
from tornado import httpclient, httputil
from tornado import gen
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
        # print self.request.body
        # print self.get_body_arguments(u'name')
        print self.request.arguments
        # email = self.get_body_arguments(u'email')
        # password = self.get_body_arguments(u'password')
        # scientist_dict = json.loads(self.get_argument(u'data', u'{}'))
        # from tests.scientist_data import Scientist
        # scientist_dict = Scientist.get_data(0)
        # print login, passw
        # scientist_id = yield ScientistBL.add_scientist(dict(email=email[0], password=password[0]))
        # response = dict(id=str(scientist_id))
        # response_data = yield self.get_response(response)
        # self.set_secure_cookie(u'scientist', str(scientist_id))
        # self.finish(response_data)

    @gen.coroutine
    def put(self):
        print u'scientist put'
        scientist_dict = json.loads(self.get_argument(u'data', u'{}'))
        yield ScientistBL.update_scientist(scientist_dict[u'scientist'])
        response_data = yield self.get_response(dict())
        self.finish(response_data)

    @gen.coroutine
    def get(self, *args, **kwargs):
        print u'scientist get'
        from tests.scientist_data import Scientist
        scientist_dict = Scientist.get_data(0)
        response = yield httpclient.AsyncHTTPClient().fetch(u'http://sciencemates.dev:9090/api/scientist/1',
                                                            body=urllib.urlencode(dict(data=json.dumps(scientist_dict))),
                                                            method=u"POST")
        json_response = json.loads(response.body)
        print json_response
        # scientist_dict = json.loads(self.get_argument(u'data', u'{}'))
        # response = yield ScientistBL.get_project(scientist_dict[u'id'])
        # response_data = yield self.get_response(response)
        # self.finish(response_data)

    @gen.coroutine
    def delete(self, scientist_id):
        print u'scientist delete'
        scientist_dict = json.loads(self.get_argument(u'data', u'{}'))
        yield ScientistBL.delete_scientist(scientist_dict[u'id'])
        response_data = yield self.get_response(dict())
        self.finish(response_data)
