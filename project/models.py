# -*- coding: utf-8 -*-

import environment
from base.models import PSQLModel

__author__ = 'oks'


class Project(PSQLModel):

    TABLE = u'projects'

    OVERVIEW_FIELDS = [u'id', u'research_fields', u'title', u'description_short', u'university_connection',
                       u'likes']

    EDITABLE_FIELDS = [u'research_fields', u'title', u'description_short', u'university_connection',
                       u'in_progress', u'objective', u'description_full', u'usage_possibilities',
                       u'results', u'related_data', u'leader', u'participants', u'vacancies',
                       u'tags', u'project_site', u'contacts']

    CREATE_FIELDS = EDITABLE_FIELDS + [u'id', u'manager_id', u'dt_created']

    SYSTEM_INFO = [u'dt_created', u'title_tsvector', u'description_short_tsvector']

    JSON_FIELDS = []

    SEARCH_MAIN_FIELDS = [u'title', u'description_short']

    SEARCH_VACANCIES = [u'vacancies']

    RELATED_TABLES = [environment.TABLE_VACANCIES, environment.TABLE_PARTICIPANTS]

    RELATED_COLUMNS = {
        # environment.TABLE_VACANCIES: [u'id', u'vacancy_name', u'description', u'difficulty'],
        environment.TABLE_VACANCIES: [u'id', u'vacancy_name', u'description'],
        environment.TABLE_PARTICIPANTS: [u'id', u'role_name', u'scientist_id', u'first_name',
                                         u'last_name', u'middle_name'],
    }

    SEARCH_FIELDS = classmethod(lambda cls, s_type: {
        u'vacancies': cls.SEARCH_VACANCIES,
        u'main': cls.SEARCH_MAIN_FIELDS
    }[s_type])