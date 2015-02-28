# -*- coding: utf-8 -*-

import momoko
from tornado import gen

from common.decorators import psql_connection
from common.exceptions import PSQLException
from db.orm import MODELS
from db.utils import get_update_sql_query, get_insert_sql_query


__author__ = 'oks'


class PSQLModel(object):

    TABLE = None

    def __init__(self, *args, **kwargs):
        super(PSQLModel, self).__init__()
        if not self.TABLE:
            raise Exception(u'TABLE is a must!')
        for key, value in MODELS[self.TABLE].iteritems():
            setattr(self, key, kwargs.get(key, value.default))

    @gen.coroutine
    @psql_connection
    def save(self, conn, update=True, fields=None):

        if fields:
            data = {k: getattr(self, k) for k in fields if hasattr(self, k)}
        else:
            data = self.__dict__

        if update:
            print self.id
            sqp_query = get_update_sql_query(self.TABLE, data, dict(id=self.id))
        else:
            sqp_query = get_insert_sql_query(self.TABLE, data)

        try:
            cursor = yield momoko.Op(conn.execute, sqp_query)
            self.id = cursor.fetchone()[0]
        except Exception, ex:
            raise PSQLException(ex)

        raise gen.Return(self.id)

    def populate_fields(self, data_dict):
        for key, value in MODELS[self.TABLE].iteritems():
            if data_dict.get(key, value.default) == getattr(self, key):
                continue
            setattr(self, key, data_dict.get(key, value.default))

    @classmethod
    @gen.coroutine
    @psql_connection
    def get_by_id(cls, conn, _id, columns=None):
        if not columns:
            columns = MODELS[cls.TABLE].keys()
        try:
            cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE id={id}".format(
                columns=u', '.join(columns),
                table_name=cls.TABLE,
                id=str(_id)))
            data = cursor.fetchone()
        except Exception, ex:
            raise PSQLException(ex)

        data = dict(zip(columns, data))
        instance = cls()
        for k, v in data.iteritems():
            if not v:
                continue
            # restore = MODELS[cls.TABLE][k].restore
            # if restore:
            #     v = restore(v)
            # if v:
            setattr(instance, k, v)

        raise gen.Return(instance)

    @classmethod
    @gen.coroutine
    @psql_connection
    def get_json_by_id(cls, conn, _id, columns=None):
        if not columns:
            columns = MODELS[cls.TABLE].keys()
        cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE id={id}".format(
            columns=u', '.join(columns),
            table_name=cls.TABLE,
            id=str(_id)))
        data = cursor.fetchone()
        data = dict(zip(columns, data))
        raise gen.Return(data)

    @classmethod
    @gen.coroutine
    @psql_connection
    def get_all_json(cls, conn, columns=None):
        if not columns:
            columns = MODELS[cls.TABLE].keys()
        cursor = yield momoko.Op(conn.execute, u'SELECT {columns} FROM {table_name}'.format(columns=u', '.join(columns),
                                                                                            table_name=cls.TABLE))
        data = cursor.fetchall()
        data_list = []
        for d in data:
            data_dict = {}
            for i, k in enumerate(columns):
                if not d[i]:
                    continue
                data_dict[k] = d[i]
            data_list.append(data_dict)
        raise gen.Return(data_list)