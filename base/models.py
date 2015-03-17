# -*- coding: utf-8 -*-

import momoko
import logging
from tornado import gen

from common.decorators import psql_connection
from common.exceptions import PSQLException
from db.orm import MODELS
from db.utils import get_update_query, get_insert_query, get_select_query, get_delete_query, get_exists_query
from common.utils import zip_values


__author__ = 'oks'


class PSQLModel(object):
    TABLE = None
    OVERVIEW_FIELDS = None
    EDITABLE_FIELDS = None
    SYSTEM_INFO = None

    def __init__(self, *args, **kwargs):
        super(PSQLModel, self).__init__()
        if not self.TABLE:
            raise Exception(u'TABLE is a must!')
        for key, value in MODELS[self.TABLE].iteritems():
            setattr(self, key, kwargs.get(key, value.default))

    @classmethod
    def get_validated_data(cls, data):
        editable_data = dict(zip_values(cls.EDITABLE_FIELDS, data, empty_fields=1))
        return editable_data

    def _get_editable_attrs(self):
        data = {}
        for k in self.EDITABLE_FIELDS:
            data[k] = getattr(self, k) or MODELS[self.TABLE][k].default
        return data

    @gen.coroutine
    @psql_connection
    def save(self, conn, update=True, fields=None):

        if fields:
            data = {k: getattr(self, k) for k in fields if hasattr(self, k)}
        else:
            data = self._get_editable_attrs()

        if update:
            sqp_query = get_update_query(self.TABLE, data, where_params=dict(id=self.id))
        else:
            sqp_query = get_insert_query(self.TABLE, data)
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
            logging.info(key)
            if key not in data_dict:
                setattr(self, key, value.default)
                logging.info('setting default')
                logging.info(key)
                logging.info(value.default)

            from_json = MODELS[self.TABLE][key].from_json
            if from_json:
                setattr(self, key, from_json(data_dict.get(key, value.default)))
            else:
                setattr(self, key, data_dict.get(key, value.default))

    @classmethod
    @gen.coroutine
    @psql_connection
    def get_from_db(cls, conn, _id, columns):
        exists_query = get_exists_query(cls.TABLE, where=dict(column=u'id', value=_id))

        try:
            cursor = yield momoko.Op(conn.execute, exists_query)
            row_exists = cursor.fetchone()[0]
        except Exception, ex:
            raise PSQLException(ex)

        if not row_exists:
            raise gen.Return({})

        try:
            sql_query = get_select_query(cls.TABLE, columns=columns, where=dict(column=u'id', value=str(_id)))
            cursor = yield momoko.Op(conn.execute, sql_query)
            data = cursor.fetchone()
        except Exception, ex:
            raise PSQLException(ex)

        raise gen.Return(data)

    @classmethod
    @gen.coroutine
    def get_by_id(cls, _id, columns=None):

        if not columns:
            columns = MODELS[cls.TABLE].keys()

        data = yield cls.get_from_db(_id, columns)

        if not data:
            raise gen.Return()

        data = dict(zip(columns, data))

        instance = cls()
        for k, v in data.iteritems():
            if not v:
                continue
            setattr(instance, k, v)

        raise gen.Return(instance)

    @classmethod
    @gen.coroutine
    def get_json_by_id(cls, _id, columns=None):

        if not columns:
            columns = MODELS[cls.TABLE].keys()

        data = yield cls.get_from_db(_id, columns)

        if not data:
            raise gen.Return({})

        data = dict(zip(columns, data))
        result_data = {}
        for k, v in data.iteritems():
            if not v:
                continue

            to_json = MODELS[cls.TABLE][k].to_json
            if to_json:
                v = to_json(v)
            result_data.update({k: v})

        raise gen.Return(result_data)

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
        logging.info(data_list)
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