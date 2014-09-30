# -*- coding: utf-8 -*-

import json
import momoko

from tornado import gen
from base.models import PSQLModel, get_insert_sql_query, get_update_sql_query
from common.decorators import psql_connection

__author__ = 'oks'


class Scientist(PSQLModel):

    PSQL_TABLE = u'scientists'
    PSQL_COLUMNS = [u'id', u'email', u'password', u'first_name', u'last_name', u'middle_name', u'dob', u'gender',
                    u'image', u'location_country', u'location_city', u'middle_education', u'high_education',
                    u'publications', u'interests', u'project_ids', u'about', u'contacts', u'desired_projects',
                    u'managing_projects', u'swear']

    def __init__(self, scientist_id):
        super(Scientist, self).__init__(scientist_id)
        self.email = u''
        self.password = u''
        self.first_name = u''
        self.last_name = u''
        self.middle_name = u''
        self.dob = u''
        self.gender = u''
        self.image = u''
        self.location_country = u''
        self.location_city = u''
        self.middle_education = []
        self.high_education = []
        self.publications = []
        self.interests = u''
        self.project_ids = []
        self.about = u''
        self.contacts = []
        self.desired_projects = []
        self.managing_projects = []
        self.swear = u''

    @classmethod
    @gen.coroutine
    def from_db_class_data(cls, scientist_id, scientist_dict):
        scientist = Scientist(scientist_id)
        for key, value in scientist_dict.iteritems():
            if value and hasattr(scientist, key):
                setattr(scientist, key, value)
        raise gen.Return(scientist)

    @classmethod
    @gen.coroutine
    @psql_connection()
    def from_db_by_id(cls, conn, scientist_id):
        cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE id={id}".format(columns=u', '.join(cls.PSQL_COLUMNS),
                                                                                                          table_name=cls.PSQL_TABLE,
                                                                                                          id=str(scientist_id)))
        scientist_data = cursor.fetchone()
        if not scientist_data:
            raise gen.Return((None, None))
        json_scientist = dict(zip(cls.PSQL_COLUMNS, scientist_data))
        scientist = yield cls.from_db_class_data(scientist_id, json_scientist)
        raise gen.Return((scientist, json_scientist))

    @classmethod
    @gen.coroutine
    @psql_connection()
    def get_all_json(cls, conn):
        cursor = yield momoko.Op(conn.execute, u'SELECT * FROM {table_name}'.format(table_name=cls.PSQL_TABLE))
        scientists_data = cursor.fetchall()
        if not scientists_data:
            raise gen.Return(None)
        json_scientists = json.dumps({'scientist': [dict(zip(cls.PSQL_COLUMNS, scientist_data)) for scientist_data in scientists_data]})
        raise gen.Return(json_scientists)

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
