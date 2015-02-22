# -*- coding: utf-8 -*-

import json
from tornado import gen, web

from base.handlers import BaseRequestHandler
from scientist.scientist_bl import ScientistBL

__author__ = 'oks'


class ScientistsListHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self):
        print u'scientists list get'
        scientists = yield ScientistBL.get_all()
        scientists = yield self.get_response(scientists)
        self.finish(json.dumps(scientists))


class ScientistHandler(BaseRequestHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        # create folder with user id
        # create folder /avatars in it
        print u'scientist post'
        scientist_dict = json.loads(self.get_argument(u'data', u'{}'))
        scientist_photo = self.request.files['photo'][0]

        scientist = yield ScientistBL.modify(scientist_dict=scientist_dict, scientist_photo=scientist_photo)

        if not isinstance(scientist_anw, dict) and u'Error' in str(scientist_anw):
            response = dict(message=scientist_anw)
            print response
            response_data = yield self.get_response(response)
            self.finish(response_data)
            return

        response_data = yield self.get_response(response)
        self.set_secure_cookie(u'scientist', str(scientist_anw))
        self.finish(response_data)

    @gen.coroutine
    def put(self):
        print u'scientist put'
        scientist_dict = json.loads(self.get_argument(u'data', u'{}'))

        yield ScientistBL.update_scientist(scientist_dict[u'scientist'])
        response_data = yield self.get_response(dict())
        self.finish(response_data)

    @gen.coroutine
    def get(self, scientist_id):
        response = yield ScientistBL.get_scientist(int(scientist_id.replace(u'/', u'')))
        response_data = yield self.get_response(response)
        print response_data
        self.finish(response_data)

    @gen.coroutine
    def delete(self, scientist_id):
        print u'scientist delete'
        yield ScientistBL.delete_scientist(scientist_id)
        response_data = yield self.get_response(dict())
        self.finish(response_data)
