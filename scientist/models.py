# -*- coding: utf-8 -*-

import json
# from momoko import Op
import momoko
from common.utils import gen_hash, set_password
from tornado import gen
from base.models import PSQLModel, get_insert_sql_query, get_update_sql_query
from common.decorators import psql_connection

__author__ = 'oks'


class Scientist(PSQLModel):

    ENTITY = u'scientist'
    TABLE = u'scientists'
    COLUMNS = [u'id', u'email', u'first_name', u'last_name', u'middle_name', u'dob', u'gender',
               u'image', u'location_country', u'location_city', u'middle_education', u'high_education',
               u'publications', u'interests', u'project_ids', u'about', u'contacts', u'desired_project_ids',
               u'managing_project_ids', u'swear']

    CHARMED = u'charmed'
    CHARMED_COLUMNS = [u'key', u'value']

    def __init__(self, scientist_id):
        super(Scientist, self).__init__(scientist_id)
        self.email = u''
        self.lang = u'Ru'
        self.first_name = u''
        self.last_name = u''
        self.middle_name = u''
        self.dob = u''
        self.gender = u''
        self.image = u''
        self.location_country = u''
        self.location_city = u''
        self.middle_education = []
        self.high_education = []    # [{country, city, university, faculty, chair, graduation_year, graduation_level}]
        self.publications = []
        self.interests = u''
        self.project_ids = []  # participate project ids
        self.about = u''
        self.contacts = []
        self.desired_project_ids = []
        self.managing_project_ids = []

        self.dt_created = None
        self.dt_last_visit = None

    @gen.coroutine
    @psql_connection
    def encrypt(self, conn, data, update=False):
        key = gen_hash(self.id, self.email)
        value = set_password(data[u'password'])
        if update:
            sqp_query, params = get_update_sql_query(self.CHARMED, dict(id=key[2], val=value))
        else:
            sqp_query, params = get_insert_sql_query(self.CHARMED, dict(id=key[2], val=value))
        yield momoko.Op(conn.execute, sqp_query, params)

    @classmethod
    def from_db_class_data(cls, scientist_id, scientist_dict):
        scientist = Scientist(scientist_id)
        for key, value in scientist_dict.iteritems():
            if hasattr(scientist, key):
                setattr(scientist, key, value)
            else:
                raise Exception(u'Unknown attribute: {}'.format(key))
        return scientist

    @classmethod
    @gen.coroutine
    @psql_connection
    def from_db_by_id(cls, conn, scientist_id):
        cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE id={id}".format(
            columns=u', '.join(cls.COLUMNS),
            table_name=cls.TABLE,
            id=str(scientist_id)))
        scientist_data = cursor.fetchone()
        if not scientist_data:
            raise gen.Return((None, None))
        json_scientist = dict(zip(cls.COLUMNS, scientist_data))
        scientist = yield cls.from_db_class_data(scientist_id, json_scientist)
        raise gen.Return((scientist, json_scientist))

    @gen.coroutine
    @psql_connection
    def save(self, conn, update=True):
        update_params = self.__dict__
        if update:
            sqp_query, params = get_update_sql_query(self.TABLE, update_params, dict(id=self.id))
        else:
            update_params.update(dict(id=self.id))
            sqp_query, params = get_insert_sql_query(self.TABLE, update_params)
        yield momoko.Op(conn.execute, sqp_query, params)
