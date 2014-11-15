# -*- coding: utf-8 -*-

import json
import momoko
from tornado import gen
from common.decorators import psql_connection

__author__ = 'oks'


class PSQLModel(object):

    ENTITY = None
    TABLE = None
    COLUMNS = None

    def __init__(self, entity_id):
        self.id = entity_id
        self.table = self.TABLE
        self.columns = self.COLUMNS
        self.initialize()

    def initialize(self):
        assert self.table, u'PSQL table name not specified'
        assert self.columns, u'PSQL columns name not specified'

    @property
    def type(self):
        return self.__class__.__name__

    def refresh_related_objects(self):
        # must implement in child-class
        pass

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


def get_insert_sql_query(tbl, insert_data):
    print insert_data
    sql_fields = u""
    sql_values = u""
    for i, title in enumerate(insert_data.keys()):
        sql_fields = u"{prefix} {title}".format(prefix=sql_fields, title=title)
        sql_values = u"{prefix} %({title})s".format(prefix=sql_values, title=title)
        if i < len(insert_data.keys()) - 1:
            sql_fields += u','
            sql_values += u','
    sql_string = u'INSERT INTO {table_name} ({fields}) VALUES ({values}) RETURNING id'.format(table_name=tbl, fields=sql_fields, values=sql_values)
    return sql_string, insert_data
