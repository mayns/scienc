# -*- coding: utf-8 -*-

from tornado import gen
from common.decorators import redis_connection

__author__ = 'oks'


class RedisModel(object):
    REDIS_KEY = u"General"

    def __init__(self, entity_id):
        self.entity_id = entity_id

    @property
    def type(self):
        return self.__class__.__name__

    def refresh_related_objects(self):
        # must implement in child-class
        pass

    @classmethod
    @gen.coroutine
    def from_redis_by_id(cls, *args):
        # abstract method
        raise NotImplementedError()

    @classmethod
    @redis_connection()
    def remove_from_redis(cls, conn, entity_id):
        yield gen.Task(conn.delete, u"{name}:{id}".format(name=cls.REDIS_KEY, id=entity_id))

    @redis_connection()
    def update_entity(self, **kwargs):
        pass


class PSQLModel(object):
    PSQL_TABLE = None
    PSQL_COLUMNS = None

    def __init__(self, entity_id):
        self.id = entity_id
        self.psql_table = self.PSQL_TABLE
        self.psql_columns = self.PSQL_COLUMNS
        self.initialize()

    def initialize(self):
        assert self.psql_table, u'PSQL table name not specified'
        assert self.psql_columns, u'PSQL columns name not specified'

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
    sql_fields = u""
    sql_values = u""
    for i, title in enumerate(insert_data.keys()):
        sql_fields = u"{prefix} {title}".format(prefix=sql_fields, title=title)
        sql_values = u"{prefix} %({title})s".format(prefix=sql_values, title=title)
        if i < len(insert_data.keys()) - 1:
            sql_fields += u','
            sql_values += u','
    sql_string = u'INSERT INTO {table_name} ({fields}) VALUES ({values})'.format(table_name=tbl, fields=sql_fields, values=sql_values)
    return sql_string, insert_data
