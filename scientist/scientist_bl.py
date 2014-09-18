# -*- coding: utf-8 -*-
import momoko

from tornado import gen
import settings
from common.decorators import redis_connection
from common.psql_connections import PSQLNonTransactionClient
from common.utils import set_password, generate_id
from common.decorators import psql_connection
from scientist.models import Scientist

__author__ = 'oks'


class ScientistBL(object):

    @classmethod
    @gen.coroutine
    @redis_connection()
    def save_to_redis(cls, conn, data):
        email = data.get(u'email', None)
        if not email:
            return
        password = data.get(u'password', None)
        if not password:
            return
        enc_password = set_password(password)
        yield gen.Task(conn.set, u'User:Email:{}'.format(email), enc_password)
        yield gen.Task(conn.hmset, u"Scientist:{id}".format(id=data['id']), data)


    @classmethod
    @gen.coroutine
    @redis_connection()
    def check_user_exist(cls, conn, email):
        password = yield gen.Task(conn.get, u'User:Email:{}'.format(email))
        raise gen.Return(password)

    @classmethod
    @gen.coroutine
    def add_scientist(cls, scientist_dict):
        scientist_id = 0
        try:
            scientist_id = generate_id()
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
            # scientist.middle_education = cls.get_middle_education_list(scientist_dict)
            scientist.high_education = scientist_dict.get(u'high_education', [])
            scientist.publications = scientist_dict.get(u'publications', [])
            scientist.interests = scientist_dict.get(u'interests', u'')
            scientist.project_ids = scientist_dict.get(u'project_ids', [])
            scientist.about = scientist_dict.get(u'about', u'')
            scientist.contacts = scientist_dict.get(u'contacts', [])
            # scientist = yield Scientist.from_db_class_data(scientist_id, scientist_dict)
            yield scientist.save(update=False)
        except Exception, ex:
            print u'Exception!!'
            print ex
        raise gen.Return(scientist_id)

    # @classmethod
    # @gen.coroutine
    # def get_middle_education_list(cls, scientist_dict):
    #     middle_education_list = scientist_dict.get(u'middle_education')
    #     middle_education_country = scientist_dict.get(u'middle_education_country')
    #     middle_education_city = scientist_dict.get(u'middle_education_city')
    #     middle_education_city = scientist_dict.get(u'middle_education_title')
    #     middle_education_year = scientist_dict.get(u'middle_education_year')


    @classmethod
    @gen.coroutine
    def get_all_scientists(cls):
        scientists = None
        try:
            scientists = yield Scientist.get_all_json()

        except Exception, ex:
            print u'Exception', ex
        raise gen.Return(scientists)

    @classmethod
    @gen.coroutine
    def delete_scientist(cls, scientist_id):
        conn = PSQLNonTransactionClient.get_client(partition=settings.PSQL_PARTITION_DEFAULT)
        try:
            sqp_query = u"DELETE FROM {table_name} WHERE id = '{id}'".format(table_name=u'scientists', id=scientist_id)
            yield momoko.Op(conn.execute, sqp_query)
        except Exception, ex:
            print u'Exception in delete scientist', ex