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
        json_data = {}
        c_columns = ['id', 'title', 'description_short', 'views', 'likes', 'organization_structure', 'end_date']
        columns = ",".join(c_columns)
        projects = yield Project.get_all_json(columns)
        if projects:
            json_data = [dict(zip(c_columns, entity_data)) for entity_data in projects]
            for j in json_data:
                j[u'id'] = int(j[u'id'])
                j[u'end_date'] = j[u'end_date'].strftime(u'%d-%m-%Y')
        raise gen.Return(json_data)


    @classmethod
    @gen.coroutine
    def get_project(cls, id):
        json_data = {}
        project = yield Project.from_db_by_id(id)
        if project:
            json_data = dict(zip(Project.COLUMNS, project))
            json_data[u'start_date'] = json_data[u'start_date'].strftime(u'%d-%m-%Y')
            json_data[u'end_date'] = json_data[u'end_date'].strftime(u'%d-%m-%Y')
        print json_data
        raise gen.Return(json_data)


