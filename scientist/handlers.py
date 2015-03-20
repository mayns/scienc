# -*- coding: utf-8 -*-

import json
from tornado import gen
import logging

from base.handlers import BaseRequestHandler
from scientist.scientist_bl import ScientistBL

__author__ = 'oks'


class ScientistsListHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self):
        print u'scientists list get'

        try:
            response = yield ScientistBL.get_all()
        except Exception, ex:
            logging.info('Exc on get all scientists:')
            logging.exception(ex)
            response = dict(
                message=ex.message
            )
        scientists = yield self.get_response(response)
        self.finish(json.dumps(scientists))


class ScientistHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, scientist_id):

        scientist_id = int(scientist_id.replace(u'/', u''))

        print u'get scientist:', scientist_id

        try:
            response = yield ScientistBL.get(scientist_id)
        except Exception, ex:
            logging.info('Exc on get scientist: {}'.format(scientist_id))
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def post(self, *args, **kwargs):
        print u'scientist post'

        scientist_dict = json.loads(self.get_argument(u'data', u'{}'))
        print scientist_dict
        scientist_photo = dict(
            raw_image=self.request.files.get('raw_image', []),
            raw_image_coords=scientist_dict.pop(u'raw_image_coords', {})
        )

        try:
            response = yield ScientistBL.create(scientist_dict=scientist_dict, scientist_photo=scientist_photo)
            self.set_secure_cookie(u'scientist', str(response[u'scientist_id']))
        except Exception, ex:
            logging.info('Exc on create scientist:')
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def put(self, *args, **kwargs):
        print u'scientist put'

        if not self.current_user_id:
            self.send_error(status_code=403)
            return

        scientist_dict = json.loads(self.get_argument(u'data', u'{}'))
        scientist_dict.update(
            scientist_id=self.current_user_id
        )
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
            logging.info('Exc on update scientist: {}'.format(self.current_user_id))
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def delete(self, scientist_id):
        print u'scientist delete: ', scientist_id

        try:
            yield ScientistBL.delete(int(scientist_id.replace(u'/', u'')))
            self.clear_cookie(u'scientist')
            return
        except Exception, ex:
            logging.info('Exc on delete scientist: {}'.format(scientist_id))
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)


class ScientistRoleHandler(BaseRequestHandler):

    @gen.coroutine
    def put(self, *args, **kwargs):
        pass

    @gen.coroutine
    def delete(self, project_id):
        pass