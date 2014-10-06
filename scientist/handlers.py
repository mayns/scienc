# -*- coding: utf-8 -*-

import json
import urllib
import hashlib
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
    def put(self):
        print u'scientist put'

    @gen.coroutine
    def get(self):
        print u'scientist get'

    @gen.coroutine
    def post(self, *args, **kwargs):
        print u'scientist post'
        scientist_dict = json.loads(self.request.body)
        if ScientistBL.validate_data(scientist_dict):
            scientist_id = yield ScientistBL.add_scientist(scientist_dict[u'scientist'])
        else:
            raise Exception(u'Not valid data')
        scientist_dict[u'scientist'].update(dict(id=scientist_id))
        self.finish(json.dumps(scientist_dict))

    @gen.coroutine
    def delete(self, scientist_id):
        print u'scientist delete'
        yield ScientistBL.delete_scientist(scientist_id)
        self.finish()
