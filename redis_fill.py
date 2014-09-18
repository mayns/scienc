# -*- coding: utf-8 -*-

__author__ = 'nyash myash'

from tornado import gen
import settings,hashlib,cPickle,time
from common.connections import RedisClient
# from codecs import encode



REDIS_COUNTRIES_KEY = u"Countries"
REDIS_COUNTRY_KEY = u"Country:{country_id}:{lang}"
REDIS_MAIN_CITIES_KEY = u"Country:{country_id}:Main_cities"
REDIS_CITIES_KEY = u"Country:{country_id}:Cities"
REDIS_CITY_KEY = u"Country:{country_id}:{city_id}"
REDIS_UNIVERSITIES_KEY = u"Country:{country_id}:{city_id}:Universities"
REDIS_UNIVERSITY_KEY = u"Country:{country_id}:{city_id}:{university_id}"
REDIS_FACULTIES_KEY = u"Country:{country_id}:{city_id}:{university_id}:Faculties"
REDIS_FACULTY_KEY = u"Country:{country_id}:{city_id}:{university_id}:{faculty_id}"
REDIS_CHAIRS_KEY = u"Country:{country_id}:{city_id}:{university_id}:{faculty_id}:Chairs"
REDIS_CHAIR_KEY = u"Country:{country_id}:{city_id}:{university_id}:{faculty_id}:{chair_id}"
REDIS_FILTER_KEY = u"Country:{country_id}:Filter:{filter}"


n = 234

def get_hash(fltr):
    """Returns a string of the hexdigest of the given filter name using MD5 algorithm"""
    hash_object = hashlib.md5(fltr.encode('utf-8'))
    return hash_object.hexdigest()



#TODO I think this should be One Single Function to fill Redis with all this data.

@gen.coroutine
def add_data():
    conn = RedisClient.get_client(settings.REDIS_PARTITION)
    pipe = conn.pipeline()

    #inserts total number of countries
    pipe.set(REDIS_COUNTRIES_KEY, 235)

    #inserts countries names in russian and english
    for lang in ['en', 'ru']:
        path = r'/countries/countries_{}.pkl'.format(lang)
        f = open(path, 'rb')
        countries = cPickle.load(f)
        f.close()
        for i in range(1, 236):
            for country in countries:
                if country[u'cid'] != i:
                    continue
                pipe.set(REDIS_COUNTRY_KEY.format(country_id=i, lang=lang), country[u'title'])
    yield gen.Task(pipe.execute)

    #inserts available data
    for i in range(1, n):
        path = r'/countries/{}.pkl'.format(i)
        f = open(path,'rb')
        cities = cPickle.load(f)
        f.close()
        path = r'/main_cities/main_cities_{}.pkl'.format(i)
        # inserts main cities cid's
        try:
            f = open(path, 'rb')
            main_cities = cPickle.load(f)
            f.close()
            for city in main_cities:
                pipe.sadd(REDIS_MAIN_CITIES_KEY.format(country_id=i), city['cid'])
        except IOError:
            pass
        #inserts data about cities, schools, universities, faculties and chairs
        for city in cities:
            pipe.sadd(REDIS_CITIES_KEY.format(country_id=i),city[u'cid'])
            dic = {}
            if u'region' in city.keys():
                dic[u'region'] = city[u'region']
            dic[u'title'] = city[u'title']
            if u'area' in city.keys():
                dic[u'area'] = city[u'area']
            pipe.hmset(REDIS_CITY_KEY.format(country_id=i, city_id=city[u'cid']), dic)

            if u'universities' not in city.keys():
                continue
            for university in city[u'universities']:
                pipe.sadd(REDIS_UNIVERSITIES_KEY.format(country_id=i, city_id=city[u'cid']),university[u'id'])
                pipe.set(REDIS_UNIVERSITY_KEY.format(country_id=i, city_id=city[u'cid'],
                                                      university_id=university[u'id']), university[u'title'])

                if u'faculties' not in university.keys():
                    continue
                for faculty in university[u'faculties']:
                    pipe.sadd(REDIS_FACULTIES_KEY.format(country_id=i, city_id=city[u'cid'],
                                                         university_id=university[u'id']), faculty[u'id'])
                    pipe.set(REDIS_FACULTY_KEY.format(country_id=i, city_id=city[u'cid'],
                                                         university_id=university[u'id'],
                                                         faculty_id=faculty[u'id']), faculty[u'title'])

                    if u'chairs' not in faculty.keys():
                        continue
                    for chair in faculty[u'chairs']:
                        pipe.sadd(REDIS_CHAIRS_KEY.format(country_id=i, city_id=city[u'cid'],
                                                             university_id=university[u'id'],
                                                             faculty_id=faculty[u'id']), chair[u'id'])
                        pipe.set(REDIS_CHAIR_KEY.format(country_id=i, city_id=city[u'cid'],
                         university_id=university[u'id'], faculty_id=faculty[u'id'],
                         chair_id=chair[u'id']), chair[u'title'])
        yield gen.Task(pipe.execute)
    yield gen.Task(pipe.execute)




@gen.coroutine
def add_filters():
    conn = RedisClient.get_client(settings.REDIS_PARTITION)
    for i in range(1, 234):
        pipe = conn.pipeline()
        print "Country No {number} {time}".format(number=i, time=time.ctime(time.time()))
        path = r'/countries/{}.pkl'.format(i)
        f = open(path, 'rb')
        cities = cPickle.load(f)
        f.close()
        for city in cities:
            name = city['title'].lower()
            l = len(name)
            num = 8 if l >=8 else l
            for j in range(1, num):
                fltr = get_hash(name[:j])
                pipe.sadd(REDIS_FILTER_KEY.format(country_id=i, filter=fltr), city['cid'])
        yield gen.Task(pipe.execute)