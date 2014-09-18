# -*- coding: utf-8 -*-

from tornado import gen, web
from base.handlers import BaseRequestHandler
import json
from project.project_bl import ProjectBL

__author__ = 'oks'


class ProjectNewHandler(BaseRequestHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        print 'in handler'
        self.render(u'/projects/add_project.html')


class ProjectNewDescriptionHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        print 'in handler !!!!'
        self.render(u'/projects/add_project_description.html')


class CkeditorSampleHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        print 'in handler'
        self.render(u'/ckeditor/samples/index.html')


class ProjectListHandler(BaseRequestHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        project_dict = json.loads(self.request.body)
        project_id = yield ProjectBL.add_project(project_dict[u'project'])
        project_dict[u'project'].update(dict(id=project_id))
        self.finish(json.dumps(project_dict))

    @gen.coroutine
    def get(self):
        projects = yield ProjectBL.get_all_projects()
        if projects is None:
            projects = json.dumps({'projects': []})
        self.finish(projects)