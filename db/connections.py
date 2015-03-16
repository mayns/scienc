# -*- coding: utf-8 -*-

import momoko
import psycopg2.extensions
import settings

# TODO tests for connections


class PSQLClient(object):
    def __init__(self):
        self._client = None
        self._connection_pool = None

    def __get_connection(self):
        if self._connection_pool is None:
            dsn = u'dbname={database} user={user} password={password} host={host} port={port}'.format(
                **settings.SCIENCE_DB)
            self._connection_pool = momoko.Pool(dsn=dsn, size=settings.PSQL_MIN_CONNECTIONS,
                                                max_size=settings.PSQL_MAX_CONNECTIONS)
        return self._connection_pool

    @classmethod
    def get_client(cls):
        connection = psql_client.__get_connection()
        return connection

psql_client = PSQLClient()

