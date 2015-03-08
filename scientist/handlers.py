# -*- coding: utf-8 -*-

import json
from tornado import gen

from base.handlers import BaseRequestHandler
from scientist.scientist_bl import ScientistBL

__author__ = 'oks'


class ScientistsListHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self):
        print u'scientists list get'

        try:
            response = yield ScientistBL.get_all_scientists()
        except Exception, ex:
            print 'Exc on get all scientists:', ex
            response = dict(
                message=ex.message
            )

        scientists = yield self.get_response(response)
        self.finish(json.dumps(scientists))


class ScientistHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, scientist_id):
        print u'get scientist:', scientist_id

        try:
            response = yield ScientistBL.get_scientist(int(scientist_id.replace(u'/', u'')))
        except Exception, ex:
            print 'Exc on get scientist:', scientist_id, ex
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def post(self, *args, **kwargs):
        print u'scientist post'
        scientist_dict = json.loads(self.get_argument(u'data', u'{}'))
        scientist_photo = dict(
            raw_image=self.request.files.get('raw_image', []),
            raw_image_coords=scientist_dict.pop(u'raw_image_coords', {})
        )

        try:
            response = yield ScientistBL.create(scientist_dict=scientist_dict, scientist_photo=scientist_photo)
        except Exception, ex:
            print 'Exc on create scientist:', ex
            self.send_error(status_code=403)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.set_secure_cookie(u'scientist', str(response[u'scientist_id']))
        self.finish(response_data)

    @gen.coroutine
    def put(self, *args, **kwargs):
        print u'scientist put'
        scientist_dict = json.loads(self.get_argument(u'data', u'{}'))
        scientist_photo = {}

        files = self.request.files.get('raw_image', [])

        if files:
            scientist_photo = dict(
                raw_image=files,
                raw_image_coords=scientist_dict.pop(u'raw_image_coords', {})
            )
        try:
            response = yield ScientistBL.update(scientist_dict=scientist_dict, scientist_photo=scientist_photo)
        except Exception, ex:
            print 'Exc on update scientist:', ex
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def delete(self, scientist_id):
        print u'scientist delete: ', scientist_id
        response = {}
        try:
            yield ScientistBL.delete(int(scientist_id.replace(u'/', u'')))
        except Exception, ex:
            print 'Exc on delete scientist:', scientist_id, ex
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)
