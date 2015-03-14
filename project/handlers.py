# -*- coding: utf-8 -*-

from tornado import gen
from base.handlers import BaseRequestHandler
import json
import logging
from project.project_bl import ProjectBL

__author__ = 'oks'


class CkeditorSampleHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        print u'ckeditor get'
        self.render(u'/ckeditor/samples/index.html')


class ProjectsListHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        print u'projects list get'

        try:
            response = yield ProjectBL.get_all_projects()
        except Exception, ex:
            logging.info('Exc on get all projects:')
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)


class ProjectHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, project_id):
        print u'get project:', project_id

        try:
            response = yield ProjectBL.get_project(int(project_id.replace(u'/', u'')))
        except Exception, ex:
            logging.info('Exc on get project: {}'.format(project_id))
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        project = yield self.get_response(response)
        self.finish(project)

    @gen.coroutine
    def post(self):
        print u'create project'
        project_dict = json.loads(self.get_argument(u'data', u'{}'))

        try:
            response = yield ProjectBL.create(project_dict)
        except Exception, ex:
            logging.info('Exc on create project:')
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def put(self):
        print u'update project'
        project_dict = json.loads(self.get_argument(u'data', u'{}'))

        try:
            response = yield ProjectBL.update(project_dict)
        except Exception, ex:
            logging.info('Exc on update project:')
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def delete(self, project_id):
        print u'delete project:', project_id
        response = {}

        try:
            yield ProjectBL.delete(int(project_id.replace(u'/', u'')))
        except Exception, ex:
            logging.info('Exc on delete project: {}'.format(project_id))
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)


class ProjectsLikeHandler(BaseRequestHandler):

    @gen.coroutine
    def put(self, project_id):
        print 'add like: ', project_id
        # data = json.loads(self.get_argument(u'data', u'{}'))
        response = {}
        try:
            yield ProjectBL.add_like(project_id)
        except Exception, ex:
            logging.info('Exc on add like:')
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def delete(self, project_id):
        print u'delete like in project:', project_id
        response = {}

        try:
            yield ProjectBL.delete_like(project_id)
        except Exception, ex:
            logging.info('Exc on delete like: {}'.format(project_id))
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)


class ProjectsParticipationHandler(BaseRequestHandler):

    @gen.coroutine
    def put(self, *args, **kwargs):
        print 'add participation'
        data = json.loads(self.get_argument(u'data', u'{}'))
        response = {}
        try:
            yield ProjectBL.add_participation(data)
        except Exception, ex:
            logging.info('Exc on add like:')
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def delete(self, project_id):
        print u'delete project:', project_id
        response = {}
        data = json.loads(self.get_argument(u'data', u'{}'))

        try:
            yield ProjectBL.delete_participation(data)
        except Exception, ex:
            logging.info('Exc on delete like: {}'.format(project_id))
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)
