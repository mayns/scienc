# -*- coding: utf-8 -*-

import json
from tornado import gen
import logging

from base.handlers import BaseRequestHandler
from scientist.scientist_bl import ScientistBL
from scientist.models import Scientist

__author__ = 'oks'


SC_EXC = lambda scientist=None: 'Exc on get scientist: {}'.format(scientist) if scientist else \
    'Exc on get scietists'


class ScientistsSearchHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        print u'scientist search'
        search_data = json.loads(self.get_argument(u'data', u'{}'))
        try:
            response = yield Scientist.search(search_data)
        except Exception, ex:
            logging.info('Exc on search scientists:')
            logging.exception(ex)
            response = dict(
                message=ex.message
            )
        search_result = yield self.get_response(response)
        self.finish(json.dumps(search_result))


class ScientistHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        scientist_id = None
        try:
            if not any(args):
                print u'scientists list get'
                response = yield ScientistBL.get_all()
            else:
                scientist_id = args[0].replace(u'/', u'')
                print u'get scientist:', scientist_id
                response = yield ScientistBL.get(scientist_id)

        except Exception, ex:
            logging.info(SC_EXC(scientist=scientist_id))
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
        print 'FROM CLIENT:', scientist_dict
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
            yield ScientistBL.delete(scientist_id.replace(u'/', u''))
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


class ScientistManagedProjectsHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        print u'managed projects get'

        if not self.current_user_id:
            self.send_error(status_code=403)
            return

        try:
            response = yield ScientistBL.get_my_projects(self.current_user_id)
        except Exception, ex:
            logging.info('Exc on get my projects: {}'.format(self.current_user_id))
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)


class ScientistParticipationProjectsHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        print u'favorite participation projects get'

        if not self.current_user_id:
            self.send_error(status_code=403)
            return

        try:
            response = yield ScientistBL.get_participation_projects(self.current_user_id)
        except Exception, ex:
            logging.info('Exc on get my projects: {}'.format(self.current_user_id))
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)


class ScientistDesiredProjectsHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        print u'favorite desired projects get'

        if not self.current_user_id:
            self.send_error(status_code=403)
            return

        try:
            response = yield ScientistBL.get_desired_projects(self.current_user_id)
        except Exception, ex:
            logging.info('Exc on get my projects: {}'.format(self.current_user_id))
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)