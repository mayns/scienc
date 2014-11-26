# -*- coding: utf-8 -*-

import momoko
from tornado import gen
import settings
from common.utils import set_password, check_password
from common.decorators import psql_connection
from scientist.models import Scientist

__author__ = 'oks'


class ScientistBL(object):

    @classmethod
    def validate_data(cls, data):
        pass

    @classmethod
    @gen.coroutine
    @psql_connection
    def check_scientist(cls, conn, email, passw):
        print set_password(passw)
        cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE id='{id}'".format(
            columns=u', '.join(Scientist.CHARMED_COLUMNS),
            table_name=Scientist.CHARMED,
            id=email))
        enc_passw = cursor.fetchone()
        if not enc_passw:
            raise gen.Return()
        exists = check_password(passw, enc_passw)
        if exists:
            cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE email='{email}'".format(
                columns=u'id',
                table_name=Scientist.TABLE,
                email=email))
        id = cursor.fetchone()
        raise gen.Return(id)

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
    def get_scientist(cls, scientist_id):
        json_scientist = yield Scientist.from_db_by_id(scientist_id)
        raise gen.Return(json_scientist)

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