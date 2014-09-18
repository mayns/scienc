# -*- coding: utf-8 -*-

import settings,hashlib
from common.connections import RedisClient
from codecs import encode

__author__ = 'nyash myash'

def test():
    REDIS_FILTER_KEY = u"Country:{country_id}:Filter:{filter}"
    REDIS_CITY_KEY = u"Country:{country_id}:{city_id}"
    conn = RedisClient.get_client(settings.REDIS_PARTITION, use_async=False)
    hash_object = hashlib.md5(u'new'.encode('utf-8  '))
    cities = conn.smembers(REDIS_FILTER_KEY.format(country_id=9, filter=hash_object.hexdigest()))
    for city in cities:
        city_name = conn.hget(REDIS_CITY_KEY.format(country_id=9, city_id=city), 'title')
        print city_name


