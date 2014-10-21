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
    COLUMNS = [u'id', u'manager', u'research_fields', u'title', u'description_short', u'views', u'likes', u'responses',
               u'organization_type', u'organization_structure', u'start_date', u'end_date', u'objective',
               u'description_full', u'usage_possibilities', u'results', u'related_data', u'leader', u'participants',
               u'missed_participants', u'tags', u'contact_manager', u'contacts', u'project_site']

    def __init__(self, project_id):
        super(Project, self).__init__(project_id)
        self.scientist_id = None     # person added the project
        self.research_fields = []  # области науки
        self.title = u''
        self.description_short = u''  # краткое описание для обложки
        self.views = 0  # количество просмотров
        self.likes = 0  # количество лайков
        self.responses = []  # ids отклкнувшихся юзеров
        self.organization_type = u''  # личный, групповой, под эгидой организации, университет
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


    @classmethod
    @gen.coroutine
    def from_db_class_data(cls, project_id, project_dict):
        project = Project(project_id)
        for key, value in project_dict.iteritems():
            if value and hasattr(project, key):
                setattr(project, key, value)
        raise gen.Return(project)

    @classmethod
    @gen.coroutine
    @psql_connection()
    def from_db_by_id(cls, conn, project_id):
        cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE id={id}".format(
            columns=u', '.join(cls.PSQL_COLUMNS),
            table_name=cls.PSQL_TABLE,
            id=str(project_id)))
        project_data = cursor.fetchone()
        if not project_data:
            raise gen.Return((None, None))
        json_project = dict(zip(cls.PSQL_COLUMNS, project_data))
        project = yield cls.from_db_class_data(project_id, json_project)
        raise gen.Return((project, json_project))

    @gen.coroutine
    @psql_connection()
    def save(self, conn, update=True):
        update_params = self.__dict__
        if update:
            sqp_query, params = get_update_sql_query(self.psql_table, update_params, dict(id=self.id))
        else:
            update_params.update(dict(id=self.id))
            sqp_query, params = get_insert_sql_query(self.psql_table, update_params)
        yield momoko.Op(conn.execute, sqp_query, params)
