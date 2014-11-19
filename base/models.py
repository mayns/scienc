# -*- coding: utf-8 -*-

import json
import momoko
from tornado import gen
from common.utils import zip_values
from common.decorators import psql_connection

__author__ = 'oks'


class PSQLModel(object):

    ENTITY = None
    TABLE = None
    COLUMNS = None

    def __init__(self):
        self.id = None

    @property
    def type(self):
        return self.__class__.__name__

    @classmethod
    @gen.coroutine
    def from_db_by_id(cls, *args):
        # abstract method
        raise NotImplementedError()

    @classmethod
    @gen.coroutine
    @psql_connection
    def get_all_json(cls, conn):
        print cls.TABLE
        cursor = yield momoko.Op(conn.execute, u'SELECT * FROM {table_name}'.format(table_name=cls.TABLE))
        data = cursor.fetchall()
        if not data:
            raise gen.Return(None)
        json_data = json.dumps({cls.ENTITY: [dict(zip(cls.COLUMNS, entity_data)) for entity_data in data]})
        raise gen.Return(json_data)


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


def get_insert_sql_query(tbl, columns, insert_data):

    """

    :param insert_data:
    :type insert_data: dict
    :return: valid SQL request query
    :rtype: unicode
    """
    colvals = zip_values(columns, insert_data)
    fields = u", ".join([v[0] for v in colvals])
    colvals = map(lambda x: (x[0], json.dumps(x[1]).replace(u'[', u'{').replace(u']', u'}')) if type(x[1]) in [list, dict, int] else x, colvals)
    values = u"'" + u"', '".join([v[1] for v in colvals]) + u"'" if len(colvals) > 1 else u"'{}'".format(colvals[0][1])
    values = values.replace(u'%', u'%%')
    sql_string = u'INSERT INTO {table_name} ({fields}) VALUES ({values}) RETURNING id'.format(table_name=tbl,
                                                                                              fields=fields,
                                                                                              values=values)
    return sql_string
