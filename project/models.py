# -*- coding: utf-8 -*-

from tornado import gen
from base.models import PSQLModel

__author__ = 'oks'


class Project(PSQLModel):

    TABLE = u'projects'

    OVERVIEW_FIELDS = [u'id', u'research_fields', u'title', u'description_short', u'university_connection',
                       u'likes']


    @classmethod
    def from_dict_data(cls, project_dict):
        project = Project()
        for key, value in project_dict.iteritems():
            if hasattr(project, key):
                setattr(project, key, value)
            else:
                raise Exception(u'Unknown attribute: {}'.format(key))
        return project

    @classmethod
    @gen.coroutine
    def from_db_class_data(cls, project_id, project_dict):
        project = Project(project_id)
        for key, value in project_dict.iteritems():
            if value and hasattr(project, key):
                setattr(project, key, value)
        raise gen.Return(project)
