# -*- coding: utf-8 -*-

from tornado import gen
from base.models import PSQLModel

__author__ = 'oks'


class Project(PSQLModel):

    TABLE = u'projects'

    OVERVIEW_FIELDS = [u'id', u'research_fields', u'title', u'description_short', u'university_connection',
                       u'likes']

    EDITABLE_FIELDS = [u'research_fields', u'title', u'description_short', u'university_connection',
                       u'in_progress', u'objective', u'description_full', u'usage_possibilities',
                       u'results', u'related_data', u'leader', u'participants', u'missed_participants',
                       u'tags', u'project_site', u'contacts']

    CREATE_FIELDS = EDITABLE_FIELDS + [u'manager_id', u'dt_created']

    SYSTEM_INFO = [u'dt_created', u'title_tsvector', u'description_short_tsvector']

    JSON_FIELDS = [u'responses', u'participants', u'missed_participants']

    SEARCH_MAIN_FIELDS = u'title'

    SEARCH_VACANCIES = [u'vacancies']

    SEARCH_FIELDS = classmethod(lambda cls, s_type: {
        u'vacancies': cls.SEARCH_VACANCIES,
        u'main': cls.SEARCH_MAIN_FIELDS
    }[s_type])