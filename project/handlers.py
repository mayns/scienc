# -*- coding: utf-8 -*-

from tornado import gen
from base.handlers import BaseRequestHandler
import json
import logging
from project.project_bl import ProjectBL
from project.models import Project

PROJECT_EXC = lambda project_id=None: 'Exc on get project: {}'.format(project_id) if project_id else \
    'Exc on get projects'

__author__ = 'oks'


# class CkeditorSampleHandler(BaseRequestHandler):
#     @gen.coroutine
#     def get(self, *args, **kwargs):
#         print u'ckeditor get'
#         self.render(u'/ckeditor/samples/index.html')


class ProjectsSearchHandler(BaseRequestHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        print u'search projects'
        search_data = json.loads(self.get_argument(u'data', u'{}'))
        print search_data
        try:
            response = yield Project.search(search_data[u's_type'], search_data[u's_query'])
        except Exception, ex:
            logging.info('Exc on search projects:')
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        search_result = yield self.get_response(response)
        self.finish(search_result)


class ProjectHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        project_id = None
        try:
            if not any(args):
                print u'projects list get'
                response = yield ProjectBL.get_all()
            else:
                project_id = args[0].replace(u'/', u'')
                print u'get project:', project_id
                response = yield ProjectBL.get(project_id)

        except Exception, ex:
            logging.info(PROJECT_EXC(project_id=project_id))
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        project = yield self.get_response(response)
        self.finish(project)

    @gen.coroutine
    def post(self, *args, **kwargs):
        print u'create project'
        project_dict = json.loads(self.get_argument(u'data', u'{}'))
        if u'in_progress' in project_dict:
            project_dict.update(in_progress='true')
        else:
            project_dict.update(in_progress='false')

        manager_id = self.current_user_id
        if not manager_id:
            self.send_error(status_code=403)
            return
        project_dict.update(manager_id=manager_id)
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
    def put(self, project_id):
        print u'update project'
        try:
            project_id = project_id.replace(u'/', u'')
        except:
            self.send_error(status_code=403)
            return
        project_dict = json.loads(self.get_argument(u'data', u'{}'))
        if u'in_progress' in project_dict:
            project_dict.update(in_progress='true')
        else:
            project_dict.update(in_progress='false')

        try:
            response = yield ProjectBL.update(project_id, project_dict)
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
        project_id = project_id.replace(u'/', u'')
        try:
            yield ProjectBL.delete(project_id)
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
        scientist_id = self.current_user_id
        if not scientist_id:
            return
        response = {}
        try:
            yield ProjectBL.add_like(project_id, scientist_id)
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
        scientist_id = self.current_user_id
        try:
            yield ProjectBL.delete_like(project_id, scientist_id)
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
    def post(self, project_id, **kwargs):
        print 'add participation'

        data = json.loads(self.get_argument(u'data', u'{}'))
        print data
        if not self.current_user_id:
            self.send_error(status_code=403)
            return
        data.update(scientist_id=self.current_user_id,
                    project_id=project_id
        )
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
        if not self.current_user_id:
            self.send_error(status_code=403)
            return
        data.update(scientist_id=self.current_user_id)
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


class ResponseHandler(BaseRequestHandler):

    @gen.coroutine
    def post(self, project_id, **kwargs):
        print 'response handler', project_id

        data = json.loads(self.get_argument(u'data', u'{}'))
        if not self.current_user_id:
            self.send_error(status_code=403)

        print data

        data.update(project_id=project_id)
        response = {}
        try:
            yield ProjectBL.update_response(data)

        except Exception, ex:
            logging.info('Exc on accept response:')
            logging.exception(ex)
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)