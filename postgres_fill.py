# -*- coding: utf-8 -*-

__author__ = 'nyash myash'

from tornado import gen
import momoko
import psycopg2
import time
from common.connections import PSQLClient
import cPickle

# TODO new tables
@gen.coroutine
def insert_data():
    conn = PSQLClient.get_client()

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
            yield momoko.Op(conn.execute, u"""INSERT INTO countries (title_en, title_ru) VALUES
                                        ('{0}', '{1}');""".format(title_en, title_ru))

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
                    city_id = yield momoko.Op(conn.execute, u"""INSERT INTO cities (country_id, title) VALUES
                                        ({country_id}, '{title}') RETURNING id;""".format(country_id = i,
                                                                                          title=city_title))
                elif not region:
                    city_id = yield momoko.Op(conn.execute, u"""INSERT INTO cities (country_id, area, title) VALUES
                                        ({country_id},'{area}','{title}') RETURNING id;""".format(country_id = i,
                                                                                       area=area, title=city_title))
                elif not area:
                    city_id = yield momoko.Op(conn.execute, u"""INSERT INTO cities (country_id, region, title) VALUES
                                        ({country_id},'{region}', '{title}') RETURNING id;""".format(country_id = i,
                                                                                    region=region, title=city_title))
                else:
                    city_id = yield momoko.Op(conn.execute, u"""INSERT INTO cities (country_id, region, area, title)
                                         VALUES ({country_id},'{region}', '{area}', '{title}')
                                         RETURNING id;""".format(country_id = i, region=region, area=area,
                                                                title=city_title))
                city_id = city_id.fetchone()[0]


                #inserting main cities
                for item in main_cities:
                    if city[u'cid'] == item[u'cid']:
                        yield momoko.Op(conn.execute, u"""INSERT INTO main_cities (country_id, city_id, title) VALUES
                                    ({country_id},{city_id}, '{title}');""".format(country_id = i, city_id = city_id,
                                                                                      title=city_title))

                #inserting schools
                if u'schools' in keys:
                    schools = city[u'schools']
                    for school in schools:
                        school_title = school[u'title']
                        if "'" in school_title:
                            school_title = school_title.replace(r"'","''")
                        yield momoko.Op(conn.execute, u"""INSERT INTO schools (city_id, title) VALUES
                                    ({city_id}, '{title}');""".format(city_id = city_id, title=school_title))

                #inserting universities
                if u'universities' in keys:
                    universities = city[u'universities']
                    for university in universities:
                        university_title = university[u'title']
                        if "'" in university_title:
                            university_title = university_title.replace(r"'","''")
                        university_id = yield momoko.Op(conn.execute, u"""INSERT INTO universities (city_id, title)
                                        VALUES ({city_id}, '{title}')  RETURNING id;""".format(city_id=city_id,
                                                                                               title=university_title))
                        university_id = university_id.fetchone()[0]


                        #inserting faculties
                        uni_keys = university.keys()
                        if u'faculties' in uni_keys:
                            faculties = university[u'faculties']
                            for faculty in faculties:
                                faculty_title = faculty[u'title']
                                if "'" in faculty_title:
                                    faculty_title = faculty_title.replace(r"'","''")
                                faculty_id = yield momoko.Op(conn.execute, u"""INSERT INTO faculties (university_id, title)
                                             VALUES ({university_id},'{title}')
                                             RETURNING id;""".format(university_id=university_id, title=faculty_title))
                                faculty_id = faculty_id.fetchone()[0]

                                #inserting chairs
                                fac_keys = faculty.keys()
                                if u'chairs' in fac_keys:
                                    chairs = faculty[u'chairs']
                                    for chair in chairs:
                                        chair_title = chair[u'title']
                                        if "'" in chair_title:
                                            chair_title = chair_title.replace(r"'","''")
                                        yield momoko.Op(conn.execute, u"""INSERT INTO chairs (faculty_id, title) VALUES
                                            ({faculty_id}, '{title}');""".format(faculty_id=faculty_id,
                                                                                      title=chair_title))

    except (psycopg2.Warning, psycopg2.Error) as error:
        raise Exception(str(error))

@gen.coroutine
def delete_kinder_garden():
    try:
        conn = PSQLClient.get_client()
        yield momoko.Op(conn.execute, u"""DELETE FROM schools WHERE (title like '%%дет. сад%%' and title not like '%%шк.%%'
                    and title not like '%%школ%%') or (title like '%%дет. сад%%' and (title like  '%%при%% шк.%%'
                    or title like  '%%при%% школ%%' or title like '%%Дошкольник%%'));""")
    except (psycopg2.Warning, psycopg2.Error) as error:
        raise Exception(str(error))
