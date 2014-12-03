# -*- coding: utf-8 -*-

import json
import momoko
from common.utils import gen_hash, set_password
from tornado import gen
from base.models import PSQLModel, get_insert_sql_query, get_update_sql_query
from common.decorators import psql_connection
from datetime import date, datetime

__author__ = 'oks'


class Scientist(PSQLModel):

    ENTITY = u'scientist'
    TABLE = u'scientists'
    COLUMNS = [u'email', u'first_name', u'last_name', u'middle_name', u'dob', u'gender',
               u'image_small', u'image_medium', u'image_large', u'location_country', u'location_city',
               u'middle_education', u'high_education', u'publications', u'interests', u'project_ids',
               u'about', u'contacts', u'desired_projects_ids', u'managing_projects_ids', u'dt_created', u'dt_last_visit']

    CHARMED = u'charmed'
    CHARMED_COLUMNS = [u'id', u'val']

    def __init__(self):
        super(Scientist, self).__init__()
        self.id = 0
        self.email = u''
        # self.lang = u'Ru'
        self.first_name = u''
        self.last_name = u''
        self.middle_name = u''
        self.dob = date
        self.gender = u''
        self.image_small = u''
        self.image_medium = u''
        self.image_large = u''
        self.location_country = u''
        self.location_city = u''
        self.middle_education = []
        self.high_education = []    # [{country, city, university, faculty, chair, graduation_year, graduation_level}]
        self.publications = []
        self.interests = u''
        self.project_ids = []  # participate project ids
        self.about = u''
        self.contacts = []
        self.desired_projects_ids = []
        self.managing_projects_ids = []

        self.dt_created = u''
        self.dt_last_visit = u''

    @gen.coroutine
    @psql_connection
    def encrypt(self, conn, data, update=False):
        key = self.email
        value = set_password(data[u'password'])
        if update:
            sqp_query, params = get_update_sql_query(self.CHARMED, dict(id=key[2], val=value))
        else:
            sqp_query = get_insert_sql_query(self.CHARMED, self.CHARMED_COLUMNS, dict(id=key, val=value))
        yield momoko.Op(conn.execute, sqp_query)

    @classmethod
    def from_dict_data(cls, scientist_dict):
        scientist = Scientist()
        for key, value in scientist_dict.iteritems():
            if hasattr(scientist, key):
                setattr(scientist, key, value)
            else:
                raise Exception(u'Unknown attribute: {}'.format(key))
        return scientist

    # @classmethod
    # @gen.coroutine
    # @psql_connection
    # def from_db_by_id(cls, conn, scientist_id):
    #     cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE id={id}".format(
    #         columns=u', '.join(cls.COLUMNS),
    #         table_name=cls.TABLE,
    #         id=str(scientist_id)))
    #     scientist_data = cursor.fetchone()
    #     if not scientist_data:
    #         raise gen.Return((None, None))
    #     json_scientist = dict(zip(cls.COLUMNS, scientist_data))
    #     dob = json_scientist.get(u'dob', None)
    #     if dob and isinstance(dob, datetime):
    #         json_scientist[u'dob'] = dob.strftime(u'%d-%m-%Y')
    #     # scientist = yield cls.from_dict_data(json_scientist)
    #     raise gen.Return(json_scientist)

    @gen.coroutine
    @psql_connection
    def save(self, conn, update=True):
        update_params = self.__dict__
        if update:
            sqp_query, params = get_update_sql_query(self.TABLE, self.COLUMNS, update_params, dict(id=self.id))
        else:
            sqp_query = get_insert_sql_query(self.TABLE, self.COLUMNS, update_params)
        cursor = yield momoko.Op(conn.execute, sqp_query)
        self.id = cursor.fetchone()[0]