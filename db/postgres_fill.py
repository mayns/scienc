# -*- coding: utf-8 -*-

__author__ = 'nyash myash'

import time
import cPickle

from tornado import gen
import momoko
import psycopg2

from db.connections import psql_client
from base.models import get_insert_query


INIT_TABLES = [u'roles', u'scientists', u'projects', u'vacancies', u'participants', u'responses']


# TODO new tables
@gen.coroutine
def insert_data():
    conn = psql_client.get_client()
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
            query = get_insert_query(table, data, columns)
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
                    query = get_insert_query(table, data, columns)
                    city_id = yield momoko.Op(conn.execute, query)
                elif not region:
                    columns = [u"country_id", u"area", u"title"]
                    data = {u"country_id": i, u"area": area, u"title": city_title}
                    query = get_insert_query(table, data, columns)
                    city_id = yield momoko.Op(conn.execute, query)
                elif not area:
                    columns = [u"country_id", u"region", u"title"]
                    data = {u"country_id": i, u"region": region, u"title": city_title}
                    query = get_insert_query(table, data, columns)
                    city_id = yield momoko.Op(conn.execute, query)
                else:
                    columns = [u"country_id", u"region", u"area", u"title"]
                    data = {u"country_id": i, u"region": region, u"area": area, u"title": city_title}
                    query = get_insert_query(table, data, columns)
                    city_id = yield momoko.Op(conn.execute, query)
                city_id = city_id.fetchone()[0]

                #inserting main cities
                for item in main_cities:
                    if city[u'cid'] == item[u'cid']:
                        table = u"main_cities"
                        columns = [u"country_id", u"city_id", u"title"]
                        data = {u"country_id": i, u"city_id": city_id, u"title": city_title}
                        query = get_insert_query(table, data, columns)
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
                        query = get_insert_query(table, data, columns)
                        yield momoko.Op(conn.execute, query)

                # inserting universities
                if u'universities' in keys:
                    universities = city[u'universities']
                    for university in universities:
                        university_title = university[u'title']
                        if "'" in university_title:
                            university_title = university_title.replace(r"'", "''")
                        table = u"universities"
                        columns = [u"city_id", u"title"]
                        data = {u"city_id": city_id, u"title": university_title}
                        query = get_insert_query(table, data, columns)
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
                                query = get_insert_query(table, data, columns)
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
                                        query = get_insert_query(table, data, columns)
                                        yield momoko.Op(conn.execute, query)

    except (psycopg2.Warning, psycopg2.Error) as error:
        raise Exception(str(error))


@gen.coroutine
def delete_kinder_garden():
    conn = psql_client.get_client()
    try:
        yield momoko.Op(conn.execute, u"""DELETE FROM schools WHERE (title like '%%дет. сад%%' and title not like '%%шк.%%'
                    and title not like '%%школ%%') or (title like '%%дет. сад%%' and (title like  '%%при%% шк.%%'
                    or title like  '%%при%% школ%%' or title like '%%Дошкольник%%'));""")
    except (psycopg2.Warning, psycopg2.Error) as error:
        raise Exception(str(error))


@gen.coroutine
def truncate_init_tables():
    conn = psql_client.get_client()
    query = """TRUNCATE {tables} CASCADE""".format(tables=', '.join(INIT_TABLES))
    try:
        yield momoko.Op(conn.execute, query)
    except Exception, ex:
        print ex


@gen.coroutine
def fill_init_data():
    from tests.scientist_data import Scientist
    from scientist.scientist_bl import ScientistBL

    from tests.project_data import Project
    from project.project_bl import ProjectBL

    scientist_data = Scientist.get_scientist()
    print 'Creating init scientists'
    try:
        for k, val in scientist_data.iteritems():
            yield ScientistBL.create(scientist_dict=val, test_mode=True)
    except Exception, ex:
        print ex

    project_data = Project.get_project()
    print 'Creating init projects'
    try:
        for k, val in project_data.iteritems():
            yield ProjectBL.create(val, test_mode=True)
    except Exception, ex:
        print ex