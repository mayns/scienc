# -*- coding: utf-8 -*-

import momoko
from common.utils import set_password
from tornado import gen
from base.models import PSQLModel, get_insert_sql_query, get_update_sql_query
from common.decorators import psql_connection
import environment
from orm import MODELS

__author__ = 'oks'


class Scientist(PSQLModel):

    TABLE = u'scientists'

    @gen.coroutine
    def pre_save(self):
        pass

    @gen.coroutine
    def on_modify(self, update=True):
        pass

    @gen.coroutine
    @psql_connection
    def encrypt(self, conn, data, update=False):
        key = self.email
        value = set_password(data[u'password'])
        if update:
            sqp_query, params = get_update_sql_query(self.CHARMED, dict(id=key[2], val=value))
        else:
            sqp_query = get_insert_sql_query(self.CHARMED, self.CHARMED_COLUMNS, dict(id=key, val=value))
        yield momoko.Op(conn.execute, sqp_query)