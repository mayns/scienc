# -*- coding: utf-8 -*-

import momoko
import psycopg2
import psycopg2.extensions

import psycopg2.pool

import settings


class PSQLClient(object):
    def __init__(self):
        self._client = None
        self._connection_pool = {}
        self._connection = {}


    @classmethod
    def __get_sync_key(cls, use_async):
        if use_async:
            return u'async'
        return u'sync'

    def __get_connection(self, partition, use_async):
        sync_key = self.__get_sync_key(use_async)
        _connection_pool = self._connection_pool.setdefault(sync_key, {})
        if _connection_pool.get(partition, None) is None:
            connection_params = settings.PSQL_PARTITION_MAP.get(partition, {})
            if use_async:
                dsn = u'dbname={database} user={user} password={password} host={host} port={port}'.format(**connection_params)

                def set_unicode():
                    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, _connection_pool[partition].getconn())
                    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY, _connection_pool[partition].getconn())
                _connection_pool[partition] = momoko.Pool(dsn=dsn, size=settings.PSQL_MIN_CONNECTIONS, max_size=settings.PSQL_MAX_CONNECTIONS, callback=set_unicode)
            else:
                connection_pool = psycopg2.pool.ThreadedConnectionPool(settings.PSQL_MIN_CONNECTIONS, settings.PSQL_MAX_CONNECTIONS, **connection_params)
                _connection_pool[partition] = connection_pool.getconn()
                psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, _connection_pool[partition])
                psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY, _connection_pool[partition])
        return _connection_pool[partition]

    @classmethod
    def get_client(cls, partition, use_async=True):
        connection = psql_client.__get_connection(partition, use_async)
        return connection


class PSQLNonTransactionClient(object):
    def __init__(self):
        self._client = None
        self._connection_pool = {}
        self._connection = {}


    @classmethod
    def __get_sync_key(cls, use_async):
        if use_async:
            return u'async'
        return u'sync'

    def __get_connection(self, partition, use_async):
        sync_key = self.__get_sync_key(use_async)
        _connection_pool = self._connection_pool.setdefault(sync_key, {})
        if _connection_pool.get(partition, None) is None:
            connection_params = settings.PSQL_PARTITION_MAP.get(partition, {})
            if use_async:
                dsn = u'dbname={database} user={user} password={password} host={host} port={port}'.format(**connection_params)
                def set_unicode():
                    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, _connection_pool[partition].getconn())
                    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY, _connection_pool[partition].getconn())
                    _connection_pool[partition].autocommit = True
                _connection_pool[partition] = momoko.Pool(dsn=dsn, size=settings.PSQL_MIN_CONNECTIONS, max_size=settings.PSQL_MAX_CONNECTIONS, callback=set_unicode)
            else:
                connection_pool = psycopg2.pool.ThreadedConnectionPool(settings.PSQL_MIN_CONNECTIONS, settings.PSQL_MAX_CONNECTIONS, **connection_params)
                _connection_pool[partition] = connection_pool.getconn()
                psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, _connection_pool[partition])
                psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY, _connection_pool[partition])
                _connection_pool[partition].autocommit = True
        return _connection_pool[partition]


    @classmethod
    def get_client(cls, partition, use_async=True):
        connection = psql_non_transaction_client.__get_connection(partition, use_async)
        return connection


psql_client = PSQLClient()
psql_non_transaction_client = PSQLNonTransactionClient()

