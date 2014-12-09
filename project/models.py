# -*- coding: utf-8 -*-

import json
import momoko

from tornado import gen
from base.models import PSQLModel, get_insert_sql_query, get_update_sql_query
from common.decorators import psql_connection

__author__ = 'oks'


class Project(PSQLModel):

    ENTITY = u'project'
    TABLE = u'projects'
    COLUMNS = [u'scientist_id', u'lang', u'research_fields', u'title', u'description_short', u'views', u'likes', u'responses',
               u'organization_type', u'organization_structure', u'start_date', u'end_date', u'objective',
               u'description_full', u'usage_possibilities', u'results', u'related_data', u'leader', u'participants',
               u'missed_participants', u'tags', u'contact_manager', u'contacts', u'project_site']

    def __init__(self):
        super(Project, self).__init__()
        self.scientist_id = None     # person added the project
        self.lang = u'Ru'
        self.research_fields = []  # области науки
        self.title = u''
        self.description_short = u''  # краткое описание для обложки
        self.views = 0  # количество просмотров
        self.likes = 0  # количество лайков
        self.responses = []  # ids отклкнувшихся юзеров
        self.organization_type = u''  # личный, групповой, под эгидой организации, университет
        self.organization_location = u''  # страна, город
        self.organization_structure = {}  # ~ university, faculty, chair -- только у организации и универа - hstore

        self.start_date = u''  # начало работы
        self.end_date = u''  # планиуремая дата окончания если есть
        self.objective = u''  # цель исследования
        self.description_full = u''  # полное описание
        self.usage_possibilities = u''  # возможности применения результатов
        self.results = u''  # достигнутые результаты и практическое применение
        self.related_data = []  # дополнительные данные -- [{'id', 'source', 'description'}]
        self.leader = u''  # руководитель проекта
        self.participants = []  # участники с ролями -- [{'id', 'role', 'name': str, <'user_id', 'verified': bool>}]
        self.missed_participants = []  # кого не хватает -- [{'id': int, 'role': str, 'description': str}]
        self.tags = []  # тэги

        self.contact_manager = u''  # ответственный за связь
        self.contacts = []  # способы связи -- [{'type', 'number'}]
        self.project_site = u''

        self.dt_created = None
        self.dt_updated = None


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
