# -*- coding: utf-8 -*-

import momoko
from tornado import gen

from common.decorators import psql_connection
from common.exceptions import PSQLException
from db.orm import MODELS
from db.utils import get_update_query, get_insert_query, get_select_query, get_delete_query


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
            sqp_query = get_update_query(self.TABLE, data, dict(id=self.id))
            print sqp_query
        else:
            sqp_query = get_insert_query(self.TABLE, data)

        try:
            cursor = yield momoko.Op(conn.execute, sqp_query)
            self.id = cursor.fetchone()
            print self.id,
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
            sql_query = get_select_query(cls.TABLE, columns=columns, where=dict(column=u'id', value=str(_id)))
            print sql_query
            cursor = yield momoko.Op(conn.execute, sql_query)
            data = cursor.fetchone()
        except Exception, ex:
            raise PSQLException(ex)

        if not data:
            raise gen.Return()

        data = dict(zip(columns, data))

        instance = cls()
        for k, v in data.iteritems():
            if not v:
                continue
            print k, v
            setattr(instance, k, v)

        raise gen.Return(instance)

    @classmethod
    @gen.coroutine
    @psql_connection
    def get_json_by_id(cls, conn, _id, columns=None):
        if not columns:
            columns = MODELS[cls.TABLE].keys()
        try:
            sql_query = get_select_query(cls.TABLE, columns=columns, where=dict(column=u'id', value=str(_id)))
            cursor = yield momoko.Op(conn.execute, sql_query)
            data = cursor.fetchone()
            data = dict(zip(columns, data))
        except Exception, ex:
            raise PSQLException(ex)

        for k, v in data.iteritems():

            to_json = MODELS[cls.TABLE][k].to_json
            if to_json:
                v = to_json(v)
            data.update({k: v})

        raise gen.Return(data)

    @classmethod
    @gen.coroutine
    @psql_connection
    def get_all_json(cls, conn, columns=None):
        if not columns:
            columns = MODELS[cls.TABLE].keys()

        sql_query = get_select_query(cls.TABLE, columns)
        cursor = yield momoko.Op(conn.execute, sql_query)
        data = cursor.fetchall()
        data_list = []
        for d in data:
            data_dict = {}
            for i, k in enumerate(columns):
                if not d[i]:
                    continue
                to_json = MODELS[cls.TABLE][k].to_json
                if to_json:
                    d[i] = to_json(d[i])
                data_dict.update({k: d[i]})
            data_list.append(data_dict)
        raise gen.Return(data_list)

    @classmethod
    @gen.coroutine
    @psql_connection
    def delete(cls, conn, _id, tbl):

        if not tbl:
            tbl = cls.TABLE
        try:
            sqp_query = get_delete_query(tbl, where=dict(column='id', value=_id))
            yield momoko.Op(conn.execute, sqp_query)
        except Exception, ex:
            raise PSQLException(ex)