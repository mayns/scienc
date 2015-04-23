# -*- coding: utf-8 -*-

import momoko
import logging
from tornado import gen
from datetime import datetime
from common.utils import generate_id

from common.decorators import psql_connection
from common.exceptions import PSQLException
from db.utils import *
from common.utils import zip_values


__author__ = 'oks'


class PSQLModel(object):
    TABLE = None
    OVERVIEW_FIELDS = None
    EDITABLE_FIELDS = None
    JSON_FIELDS = None
    CREATE_FIELDS = None
    SYSTEM_INFO = None
    SEARCH_FIELDS = None

    def __init__(self, *args, **kwargs):
        super(PSQLModel, self).__init__()
        if not self.TABLE:
            raise Exception(u'TABLE is a must!')
        for key, value in MODELS[self.TABLE].iteritems():
            setattr(self, key, kwargs.get(key, value.default))

    @classmethod
    def get_editable_data(cls, data, update=True):
        if update:
            editable_data = dict(zip_values(cls.EDITABLE_FIELDS, data, empty_fields=1))
        else:
            data.update(dt_created=datetime.utcnow())
            editable_data = dict(zip_values(cls.CREATE_FIELDS, data, empty_fields=1))
        return editable_data

    def get_updated_data(self, data, update=True):

        updated_data = {}

        editable_data = self.get_editable_data(data, update=update)

        for key, value in editable_data.iteritems():

            attr = getattr(self, key)

            if isinstance(value, unicode):
                value = value.encode('utf-8')

            if isinstance(value, list):
                o_value = value
                for i, v in enumerate(o_value):
                    value[i] = v.encode('utf-8') if isinstance(v, unicode) else v

            if not value:
                value = MODELS[self.TABLE][key].default

            from_json = MODELS[self.TABLE][key].from_json
            if from_json:
                value = from_json(value)

            if not cmp(value, attr):
                print 'EQ:', key, attr, value
                continue

            updated_data.update({
                key: value
            })
        print 'UPDATED DATA:', updated_data
        return updated_data

    def _get_editable_attrs(self):
        data = {}
        for k in self.EDITABLE_FIELDS:
            data[k] = getattr(self, k) or MODELS[self.TABLE][k].default
        return data

    @gen.coroutine
    @psql_connection
    def save(self, conn, update=True, fields=None, columns=None):

        if fields:
            data = {k: getattr(self, k) for k in fields if hasattr(self, k)}
        else:
            data = self._get_editable_attrs()
        if set(self.JSON_FIELDS) & set(data.keys()):
            for f in self.JSON_FIELDS:
                v = data.get(f)
                if not v:
                    continue
                [k.update(id=generate_id()) for k in v if not k.get(u'id')]
        if update:
            sqp_query = get_update_query(self.TABLE, data, where_params=dict(id=self.id),
                                         editable_columns=columns or self.EDITABLE_FIELDS)
        else:
            sqp_query = get_insert_query(self.TABLE, data, self.CREATE_FIELDS)
        try:
            cursor = yield momoko.Op(conn.execute, sqp_query)
            self.id = cursor.fetchone()[0]
        except Exception, ex:
            raise PSQLException(ex)

        raise gen.Return(self.id)

    def populate_fields(self, data_dict):
        for key, value in data_dict.iteritems():
            setattr(self, key, value)

    @classmethod
    @gen.coroutine
    @psql_connection
    def _get_from_db(cls, conn, _id, columns):
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
            columns = list(set(MODELS[cls.TABLE].keys()) - set(cls.SYSTEM_INFO))

        data = yield cls._get_from_db(_id, columns)

        if not data:
            raise gen.Return()

        data = dict(zip(columns, data))

        instance = cls()
        for k, v in data.iteritems():
            if not v:
                setattr(instance, k, MODELS[cls.TABLE][k].default)
            else:
                restore = MODELS[cls.TABLE][k].restore
                if restore:
                    try:
                        v = restore(v)
                    except:
                        pass
                setattr(instance, k, v)

        raise gen.Return(instance)

    @classmethod
    @gen.coroutine
    def get_json_by_id(cls, _id, columns=None):

        if not columns:
            columns = list(set(MODELS[cls.TABLE].keys()) - set(cls.SYSTEM_INFO))

        data = yield cls._get_from_db(_id, columns)

        if not data:
            raise gen.Return({})

        data = dict(zip(columns, data))
        result_data = {}
        for k, v in data.iteritems():
            if not v:
                v = MODELS[cls.TABLE][k].default

            restore = MODELS[cls.TABLE][k].restore
            if restore:
                try:
                    v = restore(v)
                except:
                    pass

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
            columns = list(set(MODELS[cls.TABLE].keys()) - set(cls.SYSTEM_INFO))

        sql_query = get_select_query(cls.TABLE, columns)
        cursor = yield momoko.Op(conn.execute, sql_query)
        data = cursor.fetchall()
        data_list = []
        for d in data:
            data_dict = {}
            for i, k in enumerate(columns):
                if not d[i]:
                    continue
                v = d[i]

                restore = MODELS[cls.TABLE][k].restore
                if restore:
                    try:
                        v = restore(v)
                    except:
                        pass

                to_json = MODELS[cls.TABLE][k].to_json
                if to_json:
                    v = to_json(v)

                data_dict.update({k: v})
            data_list.append(data_dict)
        logging.info(data_list)
        raise gen.Return(data_list)

    @classmethod
    @gen.coroutine
    @psql_connection
    def search(cls, conn, s_type, s_query):
        result_data = []
        final_dict = {}
        for f in cls.SEARCH_FIELDS(s_type):
            sql_query = get_search_query(cls.TABLE, f, s_query)
            cursor = yield momoko.Op(conn.execute, sql_query)
            data = cursor.fetchall()
            for d in data:
                result_data.append(dict(
                    id=int(d[0]),
                    field_value=d[1],
                    field_name=f))
        for l in result_data:
            final_dict.setdefault(l[u'id'], []).append(dict(field=l[u'field_name'], result=l[u'field_value']))
        raise gen.Return(sorted([dict(id=i, value=v) for i, v in final_dict.iteritems()], key=lambda x: len(x)))

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