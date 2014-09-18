# -*- coding: utf-8 -*-

import settings
import redis
import tornadoredis
from random import choice

__author__ = 'oks'


class NoPipelineTornadoRedisClient(tornadoredis.Client):
    def pipeline(self, transactional=False):
        # Нельзя использовать pipeline в клиенте для чтения.
        # Поскольку можно подцепить лишние данные или не получить их вообще
        raise Exception(u"Don't use pipeline in RedisClientReadOnly")


class NoPipelineStrictRedisClient(redis.StrictRedis):
    def pipeline(self, transaction=True, shard_hint=None):
        # Нельзя использовать pipeline в клиенте для чтения.
        # Поскольку можно подцепить лишние данные или не получить их вообще
        raise Exception(u"Don't use pipeline in RedisClientReadOnly")


class RedisClient(object):
    def __init__(self):
        self._client = None
        self._connection_pool = {}
        self._connection = {}

    @classmethod
    def __get_sync_key(cls, use_async):
        if use_async:
            return u'async'
        return u'sync'

    def __get_connection_pool(self, partition, use_async, is_master):
        sync_key = self.__get_sync_key(use_async)
        _connection_pool = self._connection_pool.setdefault(sync_key, {})
        if _connection_pool.get(partition, None) is None:
            if is_master:
                json_conn = settings.REDIS_PARTITION_MAP[partition][u"master"]
            else:
                if settings.REDIS_PARTITION_MAP[partition].get(u"slaves", None) is None:
                    raise Exception(u"No slaves provided: {}".format(settings.REDIS_PARTITION_MAP[partition]))
                json_conn = choice(settings.REDIS_PARTITION_MAP[partition][u"slaves"])

            if use_async:
                _connection_pool[partition] = \
                    tornadoredis.ConnectionPool(settings.REDIS_MAX_CONNECTIONS, False,
                                                host=json_conn[u'host'],
                                                port=json_conn[u'port'])
            else:
                _connection_pool[partition] = \
                    redis.ConnectionPool(max_connections=settings.REDIS_MAX_CONNECTIONS,
                                         host=json_conn[u'host'],
                                         port=json_conn[u'port'],
                                         db=json_conn[u"db"],
                                         decode_responses=True)
        return _connection_pool[partition]

    def __get_connection(self, partition, use_async, is_master):
        sync_key = self.__get_sync_key(use_async)
        _connection = self._connection.setdefault(sync_key, {})
        if _connection.get(partition, None) is None:
            if is_master:
                json_conn = settings.REDIS_PARTITION_MAP[partition][u"master"]
            else:
                if settings.REDIS_PARTITION_MAP[partition].get(u"slaves", None) is None:
                    raise Exception(u"No slaves provided: {}".format(settings.REDIS_PARTITION_MAP[partition]))
                json_conn = choice(settings.REDIS_PARTITION_MAP[partition][u"slaves"])
            if use_async:
                _connection[partition] = NoPipelineTornadoRedisClient(
                    host=json_conn[u'host'],
                    port=json_conn[u'port'])
            else:
                _connection[partition] = NoPipelineStrictRedisClient(
                    host=json_conn[u'host'],
                    port=json_conn[u'port'],
                    decode_responses=True)
        return _connection[partition]

    @classmethod
    def get_client(cls, partition, is_master=True, use_async=True, is_new_client=False):
        """
        Если используется мастер Redis partition или требуется использовать pipeline (is_new_client=True),
        то создаем новое подключение и используем Connection Pool
        """
        if is_master or is_new_client:
            connection_pool = redis_client.__get_connection_pool(partition, use_async, is_master)
            if use_async:
                return tornadoredis.Client(connection_pool=connection_pool, selected_db=0)
            else:
                return redis.StrictRedis(connection_pool=connection_pool, decode_responses=True)
        else:
            return redis_client.__get_connection(partition, use_async, is_master)


redis_client = RedisClient()