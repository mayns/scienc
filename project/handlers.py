# -*- coding: utf-8 -*-

from tornado import gen
from base.handlers import BaseRequestHandler
import json
from project.project_bl import ProjectBL
from tests.project_data import TestProject

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
        # projects = TestProject.get_list_data()
        projects = yield ProjectBL.get_all_projects()
        projects = projects if projects else []
        projects = yield self.get_response(projects)
        self.finish(json.dumps(projects))


class ProjectHandler(BaseRequestHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        project_dict = json.loads(self.get_argument(u'data', u'{}'))
        project_id = yield ProjectBL.add_project(project_dict)
        response = dict(id=project_id)
        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def get(self, *args, **kwargs):
        project_data = json.loads(self.get_argument(u'data', u'{}'))
        project = TestProject.get_project(int(project_data.get(u'id', 1)))
        # response = yield ProjectBL.get_project(project_dict[u'id'])
        project = yield self.get_response(project)
        self.finish(project)

    @gen.coroutine
    def put(self, *args, **kwargs):
        project_dict = json.loads(self.get_argument(u'data', u'{}'))
        yield ProjectBL.update_project(project_dict)
        response_data = yield self.get_response(dict())
        self.finish(response_data)

    @gen.coroutine
    def delete(self, *args, **kwargs):
        project_dict = json.loads(self.get_argument(u'data', u'{}'))
        yield ProjectBL.delete_project(project_dict[u'id'])
        response_data = yield self.get_response(project_dict)
        self.finish(response_data)