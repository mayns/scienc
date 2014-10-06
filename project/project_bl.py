# -*- coding: utf-8 -*-

from common.utils import generate_id
from project.models import Project
from tornado import gen

__author__ = 'oks'


class ProjectBL(object):
    @classmethod
    @gen.coroutine
    def add_project(cls, project_dict):
        project_id = 0
        try:
            project_id = generate_id(21)
            project = Project(project_id)
            project.title = project_dict.get(u'title', u'')
            project.objective = project_dict.get(u'objective', u'')
            project.description = project_dict.get(u'description', u'')
            project.results = project_dict.get(u'results', u'')
            project.team = project_dict.get(u'team', u'')
            yield project.save(update=False)
        except Exception, ex:
            print u'Exception!!'
            print ex
        raise gen.Return(project_id)

    @classmethod
    @gen.coroutine
    def get_all_projects(cls):
        try:
            projects = yield Project.get_all_json()
            raise gen.Return(projects)
        except Exception, ex:
            print u'Exception', ex