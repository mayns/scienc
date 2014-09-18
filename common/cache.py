# -*- coding: utf-8 -*-


import cPickle
import memcache
import hashlib
import settings

__author__ = 'mayns'


class Memcached(object):
    _instance = None

    def __init__(self):
        self.mem_client = memcache.Client([settings.MEMCACHE_SERVER], server_max_value_length=50 * 1024 * 1024)

    @classmethod
    def instance(cls):
        """
        instance(cls) -> Memcached
        """
        if Memcached._instance is None:
            Memcached._instance = Memcached()
        return Memcached._instance

    @classmethod
    def set_object_cached(cls, mem_keys, value, timeout=None):
        if timeout is None or timeout <= 0:
            timeout = settings.MEMCACHE_TIMEOUT
        if isinstance(mem_keys, unicode):
            mem_keys = mem_keys.encode('utf-8')
        if isinstance(mem_keys, list):
            cached_data = {}
            for mem_key in mem_keys:
                mem_key = hashlib.md5(mem_key).hexdigest()
                cached_data[mem_key] = cPickle.dumps(value, cPickle.HIGHEST_PROTOCOL)
            res = Memcached.instance().mem_client.set_multi(cached_data, timeout)
        else:
            res = Memcached.instance().mem_client.set(
                hashlib.md5(mem_keys).hexdigest(), cPickle.dumps(value, cPickle.HIGHEST_PROTOCOL), timeout)
        return res

    @classmethod
    def set(cls, mem_key, value, timeout=None):
        if timeout is None or timeout <= 0:
            timeout = settings.MEMCACHE_TIMEOUT
        if isinstance(mem_key, unicode):
            mem_key = mem_key.encode('utf-8')
        if isinstance(mem_key, list):
            raise NotImplementedError

        res = cls.instance().mem_client.set(mem_key, cPickle.dumps(value), timeout)
        return res

    @classmethod
    def get(cls, mem_key):
        if isinstance(mem_key, unicode):
            mem_key = mem_key.encode('utf-8')
        if isinstance(mem_key, list):
            raise NotImplementedError

        entity = cls.instance().mem_client.get(mem_key)
        if entity:
            entity = cPickle.loads(entity)
        return entity

    @classmethod
    def get_cached_object(cls, mem_keys):
        if isinstance(mem_keys, unicode):
            mem_keys = mem_keys.encode('utf-8')
        if isinstance(mem_keys, list):
            entity = Memcached.instance().mem_client.get_multi(
                [hashlib.md5(mem_key).hexdigest() for mem_key in mem_keys])
        else:
            keys = hashlib.md5(mem_keys).hexdigest()
            entity = Memcached.instance().mem_client.get(keys)
        if entity:
            entity = cPickle.loads(entity)
        return entity

    @classmethod
    def delete_cached_object(cls, mem_keys):
        if isinstance(mem_keys, unicode):
            mem_keys = mem_keys.encode('utf-8')
        if isinstance(mem_keys, list):
            Memcached.instance().mem_client.delete_multi([hashlib.md5(mem_key).hexdigest() for mem_key in mem_keys])
        else:
            Memcached.instance().mem_client.delete(hashlib.md5(mem_keys).hexdigest())

    @classmethod
    def flush_all(cls):
        Memcached.instance().mem_client.flush_all()