# -*- coding: utf-8 -*-
import momoko

from tornado import gen
import settings
from common.psql_connections import PSQLNonTransactionClient
from common.utils import set_password, generate_id
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
        yield gen.Task(conn.hmset, u"Scientist:{id}".format(id=data['id']), data)


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
        scientist_id = generate_id()
        scientist = Scientist.from_db_class_data(scientist_id, scientist_dict)
        scientist.encrypt()
        try:
            yield scientist.save(update=False)
        except Exception, ex:
            print u'Exception! in add scientist'
            print ex
        raise gen.Return(scientist_id)


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