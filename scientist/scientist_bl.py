# -*- coding: utf-8 -*-

import momoko
from tornado import gen
import settings
from common.utils import set_password
from common.decorators import psql_connection
from scientist.models import Scientist

__author__ = 'oks'


class ScientistBL(object):

    @classmethod
    @gen.coroutine
    def save_to_redis(cls, conn, data):
        email = data.get(u'email', None)
        if not email:
            return
        password = data.get(u'password', None)
        if not password:
            return
        enc_password = set_password(password)
        yield gen.Task(conn.set, u'User:Email:{}'.format(email), enc_password)
        yield gen.Task(conn.hmset, u"Scientist:{id}".format(id=data[u'id']), data)


    @classmethod
    def validate_data(cls, data):
        pass

    @classmethod
    @gen.coroutine
    def check_user_exist(cls, conn, email):
        password = yield gen.Task(conn.get, u'User:Email:{}'.format(email))
        raise gen.Return(password)

    @classmethod
    @gen.coroutine
    def add_scientist(cls, scientist_dict):
        password = scientist_dict.pop(u'password')
        scientist = Scientist.from_dict_data(scientist_dict)
        try:
            yield scientist.save(update=False)
            yield scientist.encrypt(dict(password=password))
        except Exception, ex:
            print u'Exception! in add scientist'
            print ex
        raise gen.Return(scientist.id)

    @classmethod
    @gen.coroutine
    @gen.coroutine
    def get_scientist(cls, scientist_id):
        scientist = yield Scientist.from_db_by_id(scientist_id)
        raise gen.Return(scientist)

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
    @psql_connection
    def delete_scientist(cls, conn, scientist_id):
        conn = conn.get_client(partition=settings.SCIENCE_DB)
        try:
            sqp_query = u"DELETE FROM {table_name} WHERE id = '{id}'".format(table_name=u'scientists', id=scientist_id)
            yield momoko.Op(conn.execute, sqp_query)
        except Exception, ex:
            print u'Exception in delete scientist', ex