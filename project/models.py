# -*- coding: utf-8 -*-

from tornado import gen
from base.models import PSQLModel

__author__ = 'oks'


class Project(PSQLModel):

    TABLE = u'projects'

    OVERVIEW_FIELDS = [u'id', u'research_fields', u'title', u'description_short', u'university_connection',
                       u'likes']