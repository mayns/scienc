# -*- coding: utf-8 -*-

import json

from tornado import gen
from common.utils import generate_id
from project.models import Project
from time import strftime

__author__ = 'oks'


class ProjectBL(object):
    @classmethod
    def create(cls):
        pass

    @classmethod
    def update(cls):
        pass

    @classmethod
    def delete(cls, project_id):
        pass

    @classmethod
    def validate_data(cls):
        pass

    @classmethod
    @gen.coroutine
    def get_all_projects(cls):
        projects_data = yield Project.get_all_json(columns=Project.OVERVIEW_FIELDS)
        raise gen.Return(projects_data)

    @classmethod
    @gen.coroutine
    def get_project(cls, project_id):
        json_data = {}
        raise gen.Return(json_data)


