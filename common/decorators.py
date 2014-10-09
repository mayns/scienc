# -*- coding: utf-8 -*-

import functools
import settings


__author__ = 'oks'


def redis_connection(partition=settings.REDIS_PARTITION, is_master=True, use_async=True, is_new_client=False):
    """Decorate methods with this to redis connection by partition.

    If deployment is in progress, raise DeploymentInProgress
    :param is_new_client: True if you need pipelines, then new Redis client will be created
    """
    def wrapper(function):
        @functools.wraps(function)
        def call(self, *args, **kwargs):
            from common.connections import RedisClient
            conn = RedisClient.get_client(partition, is_master, use_async, is_new_client)
            return function(self, conn, *args, **kwargs)
        return call
    return wrapper


def psql_connection(partition=settings.PSQL_PARTITION_DEFAULT, use_async=True):
    def wrapper(function):
        @functools.wraps(function)
        def call(self, *args, **kwargs):
            from common.psql_connections import PSQLClient
            conn = PSQLClient.get_client(partition, use_async)
            return function(self, conn, *args, **kwargs)
        return call
    return wrapper


def base_request(function):
    def wrapper(*args, **kwargs):
        from base.ajax_data import AJAX_STATUS_SUCCESS, AJAX_STATUS_ERROR
        response_data = dict(
            status=AJAX_STATUS_ERROR
        )
        try:
            data = function(*args, **kwargs)
            response_data = dict(
                status=AJAX_STATUS_SUCCESS
            )
            response_data.update(dict(data=data))
        except Exception, ex:
            print ex
        return response_data
    return wrapper