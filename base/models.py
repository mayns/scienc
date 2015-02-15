# -*- coding: utf-8 -*-

import json
import momoko
from tornado import gen
from common.utils import zip_values
from common.decorators import psql_connection
from orm import MODELS

__author__ = 'oks'


def get_update_sql_query(tbl, update_params, where_params=None):
    if where_params is None:
        where_params = {}

    sql_string = u"UPDATE {table_name} SET".format(table_name=tbl)
    for i, title in enumerate(update_params.keys()):
        sql_string = u"{prefix} {title}=%({title})s".format(prefix=sql_string, title=title)
        if i < len(update_params.keys()) - 1:
            sql_string += ','

    sql_string = u"{prefix} WHERE".format(prefix=sql_string)
    for i, title in enumerate(where_params.keys()):
        sql_string = u"{prefix} {title}=%({title})s".format(prefix=sql_string, title=title)
        if i < len(where_params.keys()) - 1:
            sql_string += u' AND '

    update_params.update(where_params)
    return sql_string, update_params


def get_insert_sql_query(tbl, insert_data):
    # TODO: check all PostgreSQL rules on storage data types and symbols

    """

    :type insert_data: dict
    :return: valid SQL request query
    :rtype: unicode
    """
    column_values = zip_values(MODELS[tbl].keys(), insert_data)
    fields = u", ".join([v[0] for v in column_values])
    values = []
    for value in column_values:
        store = MODELS[tbl][value[0]].store
        if not store:
            values.append(value[1])
            continue
        values.append(store(value[1]))

    values = u"'" + u"', '".join([v for v in values]) + u"'" if len(values) > 1 else u"'{}'".format(values[0])
    values = values.replace(u'%', u'%%')

    sql_string = u'INSERT INTO {table_name} ({fields}) VALUES ({values}) RETURNING id'.format(table_name=tbl,
                                                                                              fields=fields,
                                                                                              values=values)
    return sql_string


class PSQLModel(object):

    TABLE = None

    def __init__(self, *args, **kwargs):
        super(PSQLModel, self).__init__()
        if not self.TABLE:
            raise Exception(u'TABLE is a must!')
        for key, value in MODELS[self.TABLE].iteritems():
            setattr(self, key, kwargs.get(key, value.default))

    @gen.coroutine
    def pre_save(self):
        pass

    @gen.coroutine
    @psql_connection
    def save(self, conn, update=True):
        self.pre_save()

        data = self.__dict__
        if update:
            sqp_query, params = get_update_sql_query(self.TABLE, data, dict(id=self.id))
        else:
            sqp_query = get_insert_sql_query(self.TABLE, data)
        cursor = yield momoko.Op(conn.execute, sqp_query)
        self.id = cursor.fetchone()[0]

        self.on_modify()

        print self.id

    @gen.coroutine
    def on_modify(self):
        pass

    @gen.coroutine
    def on_delete(self):
        pass

    @classmethod
    @gen.coroutine
    @psql_connection
    def get_by_id(cls, conn, _id, columns=None):
        if not columns:
            columns = cls.COLUMNS
        cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE id={id}".format(
            columns=u', '.join(columns),
            table_name=cls.TABLE,
            id=str(_id)))
        data = cursor.fetchone()
        raise gen.Return(data)

    @classmethod
    @gen.coroutine
    @psql_connection
    def get_all_json(cls, conn, columns):
        cursor = yield momoko.Op(conn.execute, u'SELECT {columns} FROM {table_name}'.format(columns=u', '.join(columns),
                                                                                            table_name=cls.TABLE))
        data = cursor.fetchall()
        raise gen.Return(data)