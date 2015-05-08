# -*- coding: utf-8 -*-

import momoko
from tornado import gen
from base.models import PSQLModel
from common.decorators import psql_connection
from common.exceptions import *
from db.utils import *

__author__ = 'oks'


class Scientist(PSQLModel):

    TABLE = u'scientists'

    OVERVIEW_FIELDS = [u'id', u'first_name', u'middle_name', u'last_name', u'image_url',
                       u'location']

    EDITABLE_FIELDS = [u'first_name', u'middle_name', u'last_name', u'dob', u'gender',
                       u'image_url', u'location', u'middle_education', u'high_education',
                       u'publications', u'interests', u'about', u'contacts']

    CREATE_FIELDS = EDITABLE_FIELDS + [u'id', u'dt_created']

    SYSTEM_INFO = [u'dt_created']

    # JSON_FIELDS = [u'participating_projects', u'desired_vacancies']
    JSON_FIELDS = []

    SEARCH_MAIN_FIELDS = [u'first_name', u'middle_name', u'last_name']

    SEARCH_INTERESTS = [u'interests']

    SEARCH_FIELDS = classmethod(lambda cls, s_type: {
        u'interests': cls.SEARCH_INTERESTS,
        u'main': cls.SEARCH_MAIN_FIELDS
    }[s_type])

    @gen.coroutine
    @psql_connection
    def load_data(self, conn):
        pass