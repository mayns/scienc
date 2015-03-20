# -*- coding: utf-8 -*-

import copy
from db.orm import MODELS
from db.tables import TABLES
from common.utils import zip_values

__author__ = 'mayns'

ALL_TABLES = copy.deepcopy(MODELS)
ALL_TABLES.update(TABLES)


def get_update_query(tbl, update_params, where_params=None, editable_columns=None):
    if where_params is None:
        where_params = {}

    columns = editable_columns or ALL_TABLES[tbl].keys()
    columns = list(set(update_params.keys()).intersection(columns))
    column_values = dict(zip_values(columns, update_params, empty_fields=1))

    sql_string = u"UPDATE {table_name} SET".format(table_name=tbl)
    for i, k in enumerate(column_values.keys()):
        value = update_params[k]
            # if update_params[k] else ALL_TABLES[tbl][k].db_default
        print value
        store = ALL_TABLES[tbl][k].store
        v = value if not store else store(value)
        if v != 'NULL':
            sql_string = u"{prefix} {title}='{value}'".format(prefix=sql_string, title=k, value=v)
        else:
            sql_string = u"{prefix} {title}={value}".format(prefix=sql_string, title=k, value=v)
        if i < len(column_values.keys()) - 1:
            sql_string += ','

    sql_string = u"{prefix} WHERE".format(prefix=sql_string)
    for i, k in enumerate(where_params.keys()):
        sql_string = u"{prefix} {title}='{value}'".format(prefix=sql_string, title=k, value=where_params[k])
        if i < len(where_params.keys()) - 1:
            sql_string += u' AND '

    sql_string += ' RETURNING id'
    return sql_string


def get_insert_query(tbl, insert_data, create_columns=None):

    """

    :type insert_data: dict
    :return: valid SQL request query
    :rtype: unicode
    """
    columns = create_columns or ALL_TABLES[tbl].keys()
    column_values = zip_values(columns, insert_data)
    fields = u", ".join([v[0] for v in column_values])
    values = []

    for value in column_values:
        store = ALL_TABLES[tbl][value[0]].store
        if not store:
            values.append(value[1])
            continue
        print value[1]
        if value[1] == 'NULL':
            values.append(None)
            continue
        values.append(store(value[1]))
    print values
    values = u"'" + u"', '".join([v for v in values]) + u"'" if len(values) > 1 else u"'{}'".format(values[0])
    values = values.replace(u'%', u'%%')

    sql_string = u'INSERT INTO {table_name} ({fields}) VALUES ({values}) RETURNING id'.format(table_name=tbl,
                                                                                              fields=fields,
                                                                                              values=values)
    return sql_string


def get_select_query(tbl, columns=None, where=None, functions=None):
    if not columns:
        columns = [u'*']

    sql_string = u"SELECT {columns} FROM {table_name}".format(table_name=tbl,
                                                              columns=functions if functions else u', '.join(columns))
    if not where:
        return sql_string
    sql_string += u" WHERE {column}='{value}'".format(column=where['column'],
                                                      value=where['value'])
    return sql_string


def get_delete_query(tbl, where, resolve_constraints=''):
    sql_string = "DELETE FROM {table_name} WHERE {column}='{value}' {resolve}".format(table_name=tbl,
                                                                                      column=where['column'],
                                                                                      value=where['value'],
                                                                                      resolve=resolve_constraints)
    return sql_string


def get_exists_query(tbl, where):
    sql_string = "SELECT exists(SELECT 1 from {table_name} WHERE {column}='{value}')".format(table_name=tbl,
                                                                                             column=where['column'],
                                                                                             value=where['value'])
    return sql_string