# -*- coding: utf-8 -*-

import copy
from db.orm import MODELS
from db.tables import TABLES
from common.utils import zip_values

__author__ = 'mayns'

ALL_TABLES = copy.deepcopy(MODELS)
ALL_TABLES.update(TABLES)


def get_update_query(tbl, update_params, where_params=None, editable_columns=None, returning=u'id'):
    if where_params is None:
        where_params = {}

    columns = editable_columns or ALL_TABLES[tbl].keys()
    columns = list(set(update_params.keys()).intersection(set(columns)))
    column_values = dict(zip_values(columns, update_params, empty_fields=1))

    sql_string = u"UPDATE {table_name} SET".format(table_name=tbl)
    for i, k in enumerate(column_values.keys()):
        value = update_params[k]
        store = ALL_TABLES[tbl][k].store
        v = value if not store else store(value)

        if isinstance(v, str):
            v = v.decode('utf-8').encode('utf-8')
        else:
            v = v.encode('utf-8')
        if v != 'NULL':
            sql_string = "{prefix} {title}=E'{value}'".format(prefix=sql_string, title=k, value=v)
        else:
            sql_string = "{prefix} {title}={value}".format(prefix=sql_string, title=k, value=v)
        if i < len(column_values.keys()) - 1:
            sql_string += ','

    sql_string = "{prefix} WHERE".format(prefix=sql_string)
    for i, k in enumerate(where_params.keys()):
        sql_string = "{prefix} {title}='{value}'".format(prefix=sql_string, title=k, value=where_params[k])
        if i < len(where_params.keys()) - 1:
            sql_string += u' AND '

    returning = u'RETURNING {r_id}'.format(r_id=returning) if returning else u''
    sql_string += returning

    return sql_string


def get_insert_query(tbl, insert_data, create_columns=None, returning=u'id', q_id=None):
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
        if value[1] == 'NULL':
            values.append(None)
            continue
        values.append(store(value[1]))
    values = u"'" + u"', '".join([v for v in values]) + u"'" if len(values) > 1 else u"'{}'".format(values[0])
    values = values.replace(u'%', u'%%')

    returning = u'RETURNING {r_id}'.format(r_id=returning) if returning else u''

    sql_string = u'INSERT INTO {table_name} ({fields}) VALUES ({values}) {ret}'.format(table_name=tbl,
                                                                                       fields=fields,
                                                                                       values=values,
                                                                                       ret=returning)
    if q_id:
        sql_string = u'SELECT execute_query({q_id}, {q})'.format(q_id=q_id, q=sql_string)
    return sql_string


def get_select_query(tbl, columns=None, where=None, functions=None):
    if not columns:
        columns = [u'*']

    sql_string = u"SELECT {columns} FROM {table_name}".format(table_name=tbl,
                                                              columns=functions if functions else u', '.join(columns))
    if not where:
        return sql_string

    if isinstance(where, dict):
        sql_string += u" WHERE {column}='{value}'".format(column=where['column'],
                                                          value=where['value'])
    if isinstance(where, list):
        for i, clause in enumerate(where):
            if i == 0:
                sql_string += u" WHERE "
            sql_string += u"{column}='{value}'".format(column=clause['column'],
                                                       value=clause['value'])
            if i != len(where) - 1:
                sql_string += u" AND "
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


def get_search_query(tbl, select_field, select_query, limit_field=None, limit_num=None):
    if not any([limit_field, limit_num]):
        sql_string = "SELECT id, {s_field} FROM {table} WHERE {s_field} @@ '{s_query}'".format(
            s_field=select_field, table=tbl, s_query=select_query.encode('utf-8')
        )
        return sql_string

    sql_string = "SELECT {s_field} FROM {table} WHERE {s_field} @@ '{s_query}' ORDER BY {l_field} limit {l_num}".format(
        s_field=select_field, table=tbl, s_query=select_query, l_field=limit_field, l_num=limit_num
    )
    return sql_string