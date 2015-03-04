# -*- coding: utf-8 -*-

from tornado import gen
from base.handlers import BaseRequestHandler
import json
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
            print 'Exc on get all projects:', ex
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
            print 'Exc on get project:', project_id, ex
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
            print 'Exc on create project:', ex
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
            print 'Exc on update project:', ex
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
            yield ProjectBL.delete(project_id)
        except Exception, ex:
            print 'Exc on delete project:', project_id, ex
            response = dict(
                message=ex.message
            )

        response_data = yield self.get_response(response)
        self.finish(response_data)