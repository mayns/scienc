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
    def get(self):
        print u'projects list get'
        projects = yield ProjectBL.get_all_projects()
        if projects is None:
            projects = json.dumps({u'projects': []})
        self.finish(projects)


class ProjectHandler(BaseRequestHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        print u'project post'
        project_dict = json.loads(self.request.body)
        project_id = yield ProjectBL.add_project(project_dict[u'project'])
        self.finish(json.dumps(dict(id=project_id)))

    @gen.coroutine
    def put(self):
        print u'project put'

    @gen.coroutine
    def delete(self):
        print u'project delete'

    @gen.coroutine
    def get(self):
        print u'project get'