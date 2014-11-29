# -*- coding: utf-8 -*-

__author__ = 'nyash myash'

from tornado import gen
import momoko
import psycopg2
import time
from common.connections import PSQLClient
from base.models import get_insert_sql_query
from project.models import Project
import cPickle
from tests.project_data import TestProject

# TODO new tables
@gen.coroutine
def insert_data():
    conn = PSQLClient.get_client()
    try:
        # inserting countries names
        country_names = []
        for lang in ['en', 'ru']:
            path = r'/opt/data/countries_{}.pkl'.format(lang)
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
            table = u"countries"
            columns = [u"title_en", u"title_ru"]
            data = {u"title_en": title_en, u"title_ru": title_ru}
            query = get_insert_sql_query(table, columns, data)
            yield momoko.Op(conn.execute, query)

        # inserting all another data
        for i in range(1, 234):
            print "country No {}, time {} ".format(i, time.strftime("%c"))
            path = r'/opt/data/{}.pkl'.format(i)
            f = open(path, 'rb')
            cities = cPickle.load(f)
            f.close()
            try:
                path = r'/opt/data/main_cities/main_cities_{}.pkl'.format(i)
                f = open(path, 'rb')
                main_cities = cPickle.load(f)
                f.close()
            except IOError, ex:
                print u'IOError', ex
                continue

            #inserting cities title, area and region
            for city in cities:
                keys = city.keys()
                if u'region' in keys:
                    region = city[u'region']
                    if "'" in region:
                        region = region.replace(r"'", "''")
                else:
                    region = None
                if u'area' in keys:
                    area = city[u'area']
                    if "'" in area:
                        area = area.replace(r"'", "''")
                else:
                    area = None

                city_title = city[u'title']
                if "'" in city_title:
                    city_title = city_title.replace(r"'", "''")
                table = u"cities"
                if not region and not area:
                    columns = [u"country_id", u"title"]
                    data = {u"country_id": i, u"title": city_title}
                    query = get_insert_sql_query(table, columns, data)
                    city_id = yield momoko.Op(conn.execute, query)
                elif not region:
                    columns = [u"country_id", u"area", u"title"]
                    data = {u"country_id": i, u"area": area, u"title": city_title}
                    query = get_insert_sql_query(table, columns, data)
                    city_id = yield momoko.Op(conn.execute, query)
                elif not area:
                    columns = [u"country_id", u"region", u"title"]
                    data = {u"country_id": i, u"region": region, u"title": city_title}
                    query = get_insert_sql_query(table, columns, data)
                    city_id = yield momoko.Op(conn.execute, query)
                else:
                    columns = [u"country_id", u"region", u"area", u"title"]
                    data = {u"country_id": i, u"region": region, u"area": area, u"title": city_title}
                    query = get_insert_sql_query(table, columns, data)
                    city_id = yield momoko.Op(conn.execute, query)
                city_id = city_id.fetchone()[0]

                #inserting main cities
                for item in main_cities:
                    if city[u'cid'] == item[u'cid']:
                        table = u"main_cities"
                        columns = [u"country_id", u"city_id", u"title"]
                        data = {u"country_id": i, u"city_id": city_id, u"title": city_title}
                        query = get_insert_sql_query(table, columns, data)
                        yield momoko.Op(conn.execute, query)

                #inserting schools
                if u'schools' in keys:
                    schools = city[u'schools']
                    for school in schools:
                        school_title = school[u'title']
                        if "'" in school_title:
                            school_title = school_title.replace(r"'", "''")
                            table = u"schools"
                            columns = [u"city_id", u"title"]
                            data = {u"city_id": city_id, u"title": school_title}
                            query = get_insert_sql_query(table, columns, data)
                            yield momoko.Op(conn.execute, query)

                #inserting universities
                if u'universities' in keys:
                    universities = city[u'universities']
                    for university in universities:
                        university_title = university[u'title']
                        if "'" in university_title:
                            university_title = university_title.replace(r"'", "''")
                        table = u"universities"
                        columns = [u"city_id", u"title"]
                        data = {u"city_id": city_id, u"title": university_title}
                        query = get_insert_sql_query(table, columns, data)
                        university_id = yield momoko.Op(conn.execute, query)
                        university_id = university_id.fetchone()[0]

                        #inserting faculties
                        uni_keys = university.keys()
                        if u'faculties' in uni_keys:
                            faculties = university[u'faculties']
                            for faculty in faculties:
                                faculty_title = faculty[u'title']
                                if "'" in faculty_title:
                                    faculty_title = faculty_title.replace(r"'", "''")
                                table = u"faculties"
                                columns = [u"university_id", u"title"]
                                data = {u"university_id": university_id, u"title": faculty_title}
                                query = get_insert_sql_query(table, columns, data)
                                faculty_id = yield momoko.Op(conn.execute, query)
                                faculty_id = faculty_id.fetchone()[0]

                                #inserting chairs
                                fac_keys = faculty.keys()
                                if u'chairs' in fac_keys:
                                    chairs = faculty[u'chairs']
                                    for chair in chairs:
                                        chair_title = chair[u'title']
                                        if "'" in chair_title:
                                            chair_title = chair_title.replace(r"'", "''")
                                        table = u"chairs"
                                        columns = [u"faculty_id", u"title"]
                                        data = {u"faculty_id": faculty_id, u"title": chair_title}
                                        query = get_insert_sql_query(table, columns, data)
                                        yield momoko.Op(conn.execute, query)

    except (psycopg2.Warning, psycopg2.Error) as error:
        raise Exception(str(error))


@gen.coroutine
def delete_kinder_garden():
    conn = PSQLClient.get_client()
    try:
        yield momoko.Op(conn.execute, u"""DELETE FROM schools WHERE (title like '%%дет. сад%%' and title not like '%%шк.%%'
                    and title not like '%%школ%%') or (title like '%%дет. сад%%' and (title like  '%%при%% шк.%%'
                    or title like  '%%при%% школ%%' or title like '%%Дошкольник%%'));""")
    except (psycopg2.Warning, psycopg2.Error) as error:
        raise Exception(str(error))


@gen.coroutine
def add_test_project():
    conn = PSQLClient.get_client()
    test = TestProject.get_project(3)
    query = get_insert_sql_query(Project.TABLE, Project.COLUMNS, test)
    yield momoko.Op(conn.execute, query)
