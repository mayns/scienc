# -*- coding: utf-8 -*-

import functools
import psycopg2
from psycopg2 import extensions

__author__ = 'oks'


def psql_connection(function):
    @functools.wraps(function)
    def call(self, *args, **kwargs):
        from db.connections import PSQLClient
        conn = PSQLClient.get_client()
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY, conn)
        return function(self, conn, *args, **kwargs)
    return call


