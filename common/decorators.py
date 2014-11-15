# -*- coding: utf-8 -*-

import functools
import settings


__author__ = 'oks'


def psql_connection(function):
    @functools.wraps(function)
    def call(self, *args, **kwargs):
        from common.connections import PSQLClient
        conn = PSQLClient.get_client()
        return function(self, conn, *args, **kwargs)
    return call


