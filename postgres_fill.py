# -*- coding: utf-8 -*-

__author__ = 'nyash myash'

from tornado import gen
import logging
import momoko
import psycopg2
import time
import settings
from common.psql_connections import PSQLClient
from common.utils import generate_id
import cPickle

@gen.coroutine
def insert_data(partition):
    conn = PSQLClient.get_client(partition)

    try:
        # inserting countries names
        country_names = []
        for lang in ['en', 'ru']:
            path = r'/countries/countries_{}.pkl'.format(lang)
            f = open(path, 'rb')
            country_names.append(cPickle.load(f))
            f.close()
        for i in range(1, 236):
            for item in country_names[0]:
                if item[u'cid'] == i:
                    title_en = item[u'title']
            for item in country_names[1]:
                if item[u'cid'] == i:
                    title_ru = item[u'title']
            yield momoko.Op(conn.execute, u"""INSERT INTO countries (id, title_en, title_ru) VALUES
                                        ('{0}', '{1}', '{2}');""".format(i, title_en, title_ru))



        #inserting all another data
        for i in range(1,234):
            print "country No {}, time {} ".format(i, time.strftime("%c"))
            path = r'/countries/{}.pkl'.format(i)
            f = open(path,'rb')
            cities = cPickle.load(f)
            f.close()
            try:
                path = r'/main_cities/main_cities_{}.pkl'.format(i)
                f = open(path, 'rb')
                main_cities = cPickle.load(f)
                f.close()
            except IOError:
                continue

            #inserting cities title, area and region
            for city in cities:
                cid = generate_id()
                keys = city.keys()
                if u'region' in keys:
                    region = city[u'region']
                    if "'" in region:
                        region = region.replace(r"'","''")
                else:
                    region = None
                if u'area' in keys:
                    area = city[u'area']
                    if "'" in area:
                        area = area.replace(r"'","''")
                else:
                    area = None

                city_title = city[u'title']
                if "'" in city_title:
                    city_title = city_title.replace(r"'","''")
                if not region and not area:
                    yield momoko.Op(conn.execute, u"""INSERT INTO cities (cid, id,title) VALUES
                                        ('{cid}', '{id}', '{title}');""".format(cid=cid, id=i, title=city_title))
                elif not region:
                    yield momoko.Op(conn.execute, u"""INSERT INTO cities (cid, id, area, title) VALUES
                                        ('{cid}', '{id}','{area}','{title}');""".format(cid=cid, id=i,
                                                                                        area=area, title=city_title))
                elif not area:
                    yield momoko.Op(conn.execute, u"""INSERT INTO cities (cid, id, region, title) VALUES
                                        ('{cid}', '{id}','{region}', '{title}');""".format(cid=cid, id=i,
                                        region=region, title=city_title))
                else:
                    yield momoko.Op(conn.execute, u"""INSERT INTO cities (cid, id, region, area, title) VALUES
                                        ('{cid}', '{id}','{region}', '{area}', '{title}');""".format(cid=cid, id=i,
                                        region=region, area=area, title=city_title))

                #inserting main)cities
                for item in main_cities:
                    if city[u'cid'] == item[u'cid']:
                        mcid = generate_id()
                        yield momoko.Op(conn.execute, u"""INSERT INTO main_cities (mcid, cid) VALUES
                                    ('{mcid}', '{cid}');""".format(mcid=mcid, cid=cid))

                #inserting scholls
                if u'schools' in keys:
                    schools = city[u'schools']
                    for school in schools:
                        scid = generate_id()
                        school_title = school[u'title']
                        if "'" in school_title:
                            school_title = school_title.replace(r"'","''")
                        yield momoko.Op(conn.execute, u"""INSERT INTO schools (scid, cid, title) VALUES
                                    ('{scid}', '{cid}', '{title}');""".format(scid=scid, cid=cid, title=school_title))

                #inserting universities
                if u'universities' in keys:
                    universities = city[u'universities']
                    for university in universities:
                        uid = generate_id()
                        university_title = university[u'title']
                        if "'" in university_title:
                            university_title = university_title.replace(r"'","''")
                        yield momoko.Op(conn.execute, u"""INSERT INTO universities (uid, cid, title) VALUES
                                    ('{uid}', '{cid}', '{title}');""".format(uid=uid, cid=cid, title=university_title))

                        #inserting faculties
                        uni_keys = university.keys()
                        if u'faculties' in uni_keys:
                            faculties = university[u'faculties']
                            for faculty in faculties:
                                fid = generate_id()
                                faculty_title = faculty[u'title']
                                if "'" in faculty_title:
                                    faculty_title = faculty_title.replace(r"'","''")
                                yield momoko.Op(conn.execute, u"""INSERT INTO faculties (fid, uid, title) VALUES
                                    ('{fid}', '{uid}', '{title}');""".format(fid=fid, uid=uid, title=faculty_title))

                                #inserting chairs
                                fac_keys = faculty.keys()
                                if u'chairs' in fac_keys:
                                    chairs = faculty[u'chairs']
                                    for chair in chairs:
                                        chid = generate_id()
                                        chair_title = chair[u'title']
                                        if "'" in chair_title:
                                            chair_title = chair_title.replace(r"'","''")
                                        yield momoko.Op(conn.execute, u"""INSERT INTO chairs (chid, fid, title) VALUES
                                            ('{chid}', '{fid}', '{title}');""".format(chid=chid, fid=fid,
                                                                                      title=chair_title))


    except (psycopg2.Warning, psycopg2.Error) as error:
        raise Exception(str(error))

@gen.coroutine
def delete_kinder_garden(partition):
    try:
        conn = PSQLClient.get_client(partition)
        yield momoko.Op(conn.execute, u"""DELETE FROM schools WHERE (title like '%%дет. сад%%' and title not like '%%шк.%%'
                    and title not like '%%школ%%') or (title like '%%дет. сад%%' and (title like  '%%при%% шк.%%'
                    or title like  '%%при%% школ%%' or title like '%%Дошкольник%%'));""")
    except (psycopg2.Warning, psycopg2.Error) as error:
        raise Exception(str(error))
