# -*- coding: utf-8 -*-

import datetime
import json
import momoko

from tornado import gen
from base.models import PSQLModel, get_insert_sql_query, get_update_sql_query
from common.decorators import redis_connection, psql_connection
from common.utils import generate_id
import settings

from common.psql_connections import PSQLNonTransactionClient, PSQLClient
__author__ = 'oks'


class Scientist(PSQLModel):

    PSQL_TABLE = u'scientists'
    PSQL_COLUMNS = [u'id', u'first_name', u'last_name', u'middle_name', u'dob_day', u'dob_month', u'dob_year', u'gender', u'image',
                    u'location_country', u'location_city', u'education', u'publications', u'interests',
                    u'project_ids', u'about', u'email', u'contacts']

    def __init__(self, scientist_id):
        super(Scientist, self).__init__(scientist_id)
        self.first_name = u''             # * - mandatory field
        self.last_name = u''          # *
        self.middle_name = u''      # *
        self.dob_day = u''             #
        self.dob_month = u''             #
        self.dob_year = u''             #
        self.gender = u''
        self.image = u''           #
        self.location_country = u''        # место пребывания
        self.location_city = u''
        self.middle_education = []         # list of dicts
        self.high_education = []         # list of dicts
        self.publications = []
        self.interests = u''
        self.project_ids = []
        self.about = u''
        self.email = u''            # *
        self.contacts = []
        # self.links_to_scientists = []

        # education object/dict: {country, city, place, grad level}

    @classmethod
    @gen.coroutine
    def from_db_class_data(cls, scientist_id, scientist_dict):
        scientist = Scientist(scientist_id)
        scientist.first_name = scientist_dict.get(u'first_name', u'')
        scientist.last_name = scientist_dict.get(u'last_name', u'')
        scientist.middle_name = scientist_dict.get(u'middle_name', u'')
        scientist.dob_day = scientist_dict.get(u'dob_day', u'')
        scientist.dob_month = scientist_dict.get(u'dob_month', u'')
        scientist.dob_year = scientist_dict.get(u'dob_year', u'')
        scientist.gender = scientist_dict.get(u'gender', u'')
        scientist.image = scientist_dict.get(u'image', u'')
        scientist.location_country = scientist_dict.get(u'location_country', u'')
        scientist.location_city = scientist_dict.get(u'location_city', u'')
        scientist.middle_education = scientist_dict.get(u'middle_education', [])
        scientist.high_education = scientist_dict.get(u'high_education', [])
        scientist.publications = scientist_dict.get(u'publications', [])
        scientist.interests = scientist_dict.get(u'interests', u'')
        scientist.project_ids = scientist_dict.get(u'project_ids', [])
        scientist.about = scientist_dict.get(u'about', u'')
        scientist.contacts = scientist_dict.get(u'contacts', [])
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
        # scientist.flush_memcached()
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
    # @psql_connection()
    def save(self, update=True):
        conn = PSQLNonTransactionClient.get_client(partition=settings.PSQL_PARTITION_DEFAULT)
        update_params = dict(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            dob_day=self.dob_day,
            dob_month=self.dob_month,
            dob_year=self.dob_year,
            gender=self.gender,
            image=self.image,
            location_country=self.location_country,
            location_city=self.location_city,
            middle_education=self.middle_education,
            high_education=self.high_education,
            publications=self.publications,
            interests=self.interests,
            project_ids=self.project_ids,
            about=self.about,
            email=self.email,
            contacts=self.contacts,
        )
        if update:
            sqp_query, params = get_update_sql_query(self.psql_table, update_params, dict(id=self.id))
        else:
            update_params.update(dict(id=self.id))
            sqp_query, params = get_insert_sql_query(self.psql_table, update_params)
        yield momoko.Op(conn.execute, sqp_query, params)
        # self.flush_memcached()
        # conn.commit()
