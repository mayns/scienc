# -*- coding: utf-8 -*-

import json

from tornado import gen
from common.utils import generate_id
from project.models import Project
from time import strftime

__author__ = 'oks'


class ProjectBL(object):
    @classmethod
    @gen.coroutine
    def add_project(cls, project_dict):
        project = Project.from_dict_data(project_dict)
        try:
            yield project.save(update=False)
        except Exception, ex:
            print u'Exception! in add project', ex
        raise gen.Return(dict(id=project.id))

    @classmethod
    @gen.coroutine
    def get_all_projects(cls):
        projects_data = yield Project.get_all_json(columns=Project.OVERVIEW_FIELDS)
        raise gen.Return(projects_data)

    @classmethod
    @gen.coroutine
    def get_project(cls, id):
        json_data = {}
        project = yield Project.from_db_by_id(id)
        if project:
            json_data = dict(zip(Project.COLUMNS, project))
            if json_data[u'start_date']:
                json_data[u'start_date'] = json_data[u'start_date'].strftime(u'%d-%m-%Y')
            if json_data[u'end_date']:
                json_data[u'end_date'] = json_data[u'end_date'].strftime(u'%d-%m-%Y')
        print json_data
        raise gen.Return(json_data)


