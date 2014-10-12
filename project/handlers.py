# -*- coding: utf-8 -*-

from tornado import gen
from base.handlers import BaseRequestHandler
import json
from project.project_bl import ProjectBL
from tests.project_data import Project

__author__ = 'oks'


class CkeditorSampleHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        print u'ckeditor get'
        self.render(u'/ckeditor/samples/index.html')


class ProjectsListHandler(BaseRequestHandler):

    @gen.coroutine
    def get_payload(self, *args, **kwargs):
        print u'projects list get'
        projects = Project.get_data()
        # projects = yield ProjectBL.get_all_projects()
        if projects is None:
            projects = json.dumps({u'projects': []})
        raise gen.Return(projects)


class ProjectHandler(BaseRequestHandler):
    @gen.coroutine
    def get_payload(self, *args, **kwargs):
        print u'project post'
        project_dict = json.loads(self.get_argument(u'data', u'{}'))
        return project_dict

    @gen.coroutine
    def post(self, *args, **kwargs):
        data = yield self.get_payload(*args, **kwargs)
        project_id = yield ProjectBL.add_project(data)
        response = dict(id=project_id)
        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def get(self, *args, **kwargs):
        data = yield self.get_payload(*args, **kwargs)
        response = yield ProjectBL.get_project(data[u'id'])
        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def put(self, *args, **kwargs):
        data = yield self.get_payload()
        response_data = yield self.get_response(data)
        self.finish(response_data)

    @gen.coroutine
    def delete(self, *args, **kwargs):
        data = yield self.get_payload()
        response_data = yield self.get_response(data)
        self.finish(response_data)