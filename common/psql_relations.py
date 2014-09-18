# -*- coding: utf-8 -*-

from tornado import gen
import logging
import momoko
import psycopg2
import settings
from common.psql_connections import PSQLClient

__author__ = 'mayns'


def create_dbs():
    from psycopg2 import connect
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    dbs_params = settings.PSQL_PARTITION_MAP.keys()
    for dbs_key in dbs_params:
        dbs_param = settings.PSQL_PARTITION_MAP[dbs_key]
        root_con = connect(dbname=u'postgres', user=settings.PSQL_ROOT_USER, host=dbs_param[u'host'],
                           port=dbs_param[u'port'], password=settings.PSQL_ROOT_PASSWORD)
        root_cursor = root_con.cursor()
        root_cursor.execute(u'SELECT 1 FROM pg_roles WHERE rolname=%s', (dbs_param[u'user'],))
        exist_user = root_cursor.fetchone()
        if not exist_user:
            root_cursor.execute(u'CREATE USER {}'.format(dbs_param[u'user']))
        root_cursor.execute(u'ALTER USER {} WITH PASSWORD %s'.format(dbs_param[u'user']), (dbs_param[u'password'],))
        root_cursor.execute(u'ALTER USER {} CREATEDB'.format(dbs_param[u'user']))
        root_con.commit()
        root_con.close()

        con = connect(dbname=u'postgres', user=dbs_param[u'user'], host=dbs_param[u'host'],
                      port=dbs_param[u'port'], password=dbs_param[u'password'])
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        cursor.execute(u'SELECT 1 FROM pg_database WHERE datname=%s', (dbs_param[u'database'],))
        exist_db = cursor.fetchone()
        if not exist_db:
            cursor.execute(u'CREATE DATABASE {}'.format(dbs_param[u'database']))
        con.commit()
        con.close()


@gen.coroutine
def create_relations(partition):
    try:
        print u'creating relations'
        # yield delete_tables(partition)
        # yield delete_tables(partition)
        # logging.info(u'creating scientists')
        yield create_project_relation(partition)
        # yield create_scientists_relation(partition)
        # yield create_country_relation(partition)
        # yield create_city_relation(partition)
        # yield create_main_city_relation(partition)
        # yield create_university_relation(partition)
        # yield create_faculty_relation(partition)
        # yield create_chair_relation(partition)
        # yield create_school_relation(partition)
        logging.info(u'done')

    except (psycopg2.Warning, psycopg2.Error) as error:
        raise Exception(str(error))


@gen.coroutine
def delete_tables(partition):
        conn = PSQLClient.get_client(partition)
        logging.info(u'deleting scientists')
        yield momoko.Op(conn.execute, 'DROP TABLE scientists CASCADE')


@gen.coroutine
def create_scientists_relation(partition):
        conn = PSQLClient.get_client(partition)

        # yield momoko.Op(conn.execute, u"CREATE UNIQUE INDEX scientists_unique ON scientists (id, email);")
        yield momoko.Op(conn.execute,
                        'CREATE TABLE scientists ('
                        'id    varchar(80) primary key, '
                        'first_name text, '
                        'last_name text, '
                        'middle_name text, '
                        'dob_day text, '
                        'dob_month text, '
                        'dob_year text, '
                        'gender text, '
                        'image text, '
                        'location_country text, '
                        'location_city text, '
                        'middle_education  text[], '
                        'high_education  text[], '
                        'publications  text[], '
                        'interests  text, '
                        'project_ids  text[], '
                        'about  text, '
                        'email  text, '
                        'contacts  text[]);')

        yield momoko.Op(conn.execute, u"CREATE INDEX scientists_projects_gin ON scientists USING GIN(project_ids);")


@gen.coroutine
def create_project_relation(partition):
    conn = PSQLClient.get_client(partition)
    yield momoko.Op(conn.execute,
                    'CREATE TABLE projects ('
                    'id varchar(80) primary key,'
                    # 'sphere text,'  # область исследований
                    'title text,'  # название
                    'description text DEFAULT NULL,'  # краткое описание - выводится в карточке проекта
                    # 'short_description text DEFAULT NULL,'  # краткое описание - выводится в карточке проекта
                    # 'participants text[],'  # участники проекта с ролями - как это сделать?????
                    # 'form text,'  # личный, групповой, под эгидой организации
                    # 'sponsor_organization_type text DEFAULT NULL,'  # гражданское научное учреждение, частная компания,
                    # государственная или муниципальная компания, военное учреждение, общественная организация
                    # 'organization_name text DEFAULT NULL,'
                    'objective text,'  # цель исследваний
                    'results text,'  # описание исследований
                    'team text);')  # описание исследований
                    # 'research_description text,'  # описание исследований
                    # 'usage_facts text DEFAULT NULL,'  # результаты уже применены
                    # 'usage_possibilities text DEFAULT NULL,'  # предполагаемое применение результатов
                    # 'useful_data text DEFAULT NULL,' # полезные статьи и т.п.
                    # 'main_project_id varchar(80) DEFAULT NULL ,'  # ссылка на основной прект (если таковой есть)
                    # 'sub_project_id varchar(80) DEFAULT NULL,'  # ссылка на дополнительные проекты
                    # 'gratuities text DEFAULT NULL);')

    # yield momoko.Op(conn.execute, u"CREATE INDEX title_ru_idx ON projects "
    #                               u"USING GIN (to_tsvector('russian', title));")
    # yield momoko.Op(conn.execute, u"CREATE INDEX title_en_idx ON projects "
    #                               u"USING GIN (to_tsvector('english', title));")
    #
    # yield momoko.Op(conn.execute, u"CREATE INDEX short_description_ru_idx ON projects "
    #                               u"USING GIN (to_tsvector('russian', short_description));")
    # yield momoko.Op(conn.execute, u"CREATE INDEX short_description_en_idx ON projects "
    #                               u"USING GIN (to_tsvector('english', short_description));")
    #
    # yield momoko.Op(conn.execute, u"CREATE INDEX organization_name_ru_idx ON projects "
    #                               u"USING GIN (to_tsvector('russian', organization_name));")
    # yield momoko.Op(conn.execute, u"CREATE INDEX organization_name_en_idx ON projects "
    #                               u"USING GIN (to_tsvector('english', organization_name));")
    #
    # yield momoko.Op(conn.execute, u"CREATE INDEX purpose_ru_idx ON projects "
    #                               u"USING GIN (to_tsvector('russian', purpose));")
    # yield momoko.Op(conn.execute, u"CREATE INDEX purpose_en_idx ON projects "
    #                               u"USING GIN (to_tsvector('english', purpose));")
    #
    # yield momoko.Op(conn.execute, u"CREATE INDEX research_description_ru_idx ON projects "
    #                               u"USING GIN (to_tsvector('russian', research_description));")
    # yield momoko.Op(conn.execute, u"CREATE INDEX research_description_en_idx ON projects "
    #                               u"USING GIN (to_tsvector('english', research_description)); ")
    #
    # yield momoko.Op(conn.execute, u"CREATE INDEX sage_facts_ru_idx ON projects "
    #                               u"USING GIN (to_tsvector('russian', usage_facts));")
    # yield momoko.Op(conn.execute, u"CREATE INDEX usage_facts_en_idx ON projects "
    #                               u"USING GIN (to_tsvector('english', usage_facts));")
    #
    # yield momoko.Op(conn.execute, u"CREATE INDEX usage_possibilities_ru_idx ON projects "
    #                               u"USING GIN (to_tsvector('russian', usage_possibilities));")
    # yield momoko.Op(conn.execute, u"CREATE INDEX usage_possibilities_en_idx ON projects "
    #                               u"USING GIN (to_tsvector('english', usage_possibilities));")








@gen.coroutine
def create_country_relation(partition):
    conn = PSQLClient.get_client(partition)
    yield momoko.Op(conn.execute,
                    'CREATE TABLE countries ('
                    'id varchar(80) primary key,'
                    'title_en text,'
                    'title_ru text);')

    yield momoko.Op(conn.execute, u"CREATE INDEX countries_ru_idx ON countries "
                                  u"USING GIN(to_tsvector('russian', title_ru));")
    yield momoko.Op(conn.execute, u"CREATE INDEX countries_en_idx ON countries "
                                  u"USING GIN(to_tsvector('english', title_en));")




@gen.coroutine
def create_city_relation(partition):
    conn = PSQLClient.get_client(partition)
    yield momoko.Op(conn.execute,
                    'CREATE TABLE cities ('
                    'cid varchar(80) primary key,'
                    'id varchar(80) REFERENCES countries(id),'
                    'region text DEFAULT NULL,'
                    'area text DEFAULT NULL,'
                    'title text);')

    yield momoko.Op(conn.execute, u"CREATE INDEX region_ru_idx ON cities "
                                  u"USING GIN(to_tsvector('russian', region));")
    yield momoko.Op(conn.execute, u"CREATE INDEX region_en_idx ON cities "
                                  u"USING GIN(to_tsvector('english', region));")
    yield momoko.Op(conn.execute, u"CREATE INDEX area_ru_idx ON cities "
                                  u"USING GIN(to_tsvector('russian', area));")
    yield momoko.Op(conn.execute, u"CREATE INDEX area_en_idx ON cities "
                                  u"USING GIN(to_tsvector('english', area));")
    yield momoko.Op(conn.execute, u"CREATE INDEX cities_ru_idx ON cities "
                                  u"USING GIN(to_tsvector('russian', title));")
    yield momoko.Op(conn.execute, u"CREATE INDEX cities_en_idx ON cities "
                                  u"USING GIN(to_tsvector('english', title));")



@gen.coroutine
def create_main_city_relation(partition):
    conn = PSQLClient.get_client(partition)
    yield momoko.Op(conn.execute,
                    'CREATE TABLE main_cities ('
                    'mcid varchar(80) primary key,'
                    'cid varchar(80) REFERENCES cities (cid));')



@gen.coroutine
def create_university_relation(partition):
    conn = PSQLClient.get_client(partition)
    yield momoko.Op(conn.execute,
                    'CREATE TABLE universities ('
                    'uid varchar(80) primary key,'
                    'cid varchar(80) REFERENCES cities (cid),'
                    'title text);')
    yield momoko.Op(conn.execute, u"CREATE INDEX universities_ru_idx ON universities "
                                  u"USING GIN(to_tsvector('russian', title));")
    yield momoko.Op(conn.execute, u"CREATE INDEX universities_en_idx ON universities "
                                  u"USING GIN(to_tsvector('english', title));")


@gen.coroutine
def create_faculty_relation(partition):
    conn = PSQLClient.get_client(partition)
    yield momoko.Op(conn.execute,
                    'CREATE TABLE faculties ('
                    'fid varchar(80) primary key,'
                    'uid varchar(80) REFERENCES universities(uid),'
                    'title text);')
    yield momoko.Op(conn.execute, u"CREATE INDEX faculties_ru_idx ON faculties "
                                  u"USING GIN(to_tsvector('russian', title));")
    yield momoko.Op(conn.execute, u"CREATE INDEX faculties_en_idx ON faculties "
                                  u"USING GIN(to_tsvector('english', title));")


@gen.coroutine
def create_chair_relation(partition):
    conn = PSQLClient.get_client(partition)
    yield momoko.Op(conn.execute,
                    'CREATE TABLE chairs ('
                    'chid varchar(80) primary key,'
                    'fid varchar(80) REFERENCES faculties(fid),'
                    'title text);')
    yield momoko.Op(conn.execute, u"CREATE INDEX chairs_ru_idx ON chairs "
                                  u"USING GIN(to_tsvector('russian', title));")
    yield momoko.Op(conn.execute, u"CREATE INDEX chairs_en_idx ON chairs "
                                  u"USING GIN(to_tsvector('english', title));")

@gen.coroutine
def create_school_relation(partition):
    conn = PSQLClient.get_client(partition)
    yield momoko.Op(conn.execute,
                    'CREATE TABLE schools ('
                    'scid varchar(80) primary key,'
                    'cid varchar(80) REFERENCES cities(cid),'
                    'title text);')
    yield momoko.Op(conn.execute, u"CREATE INDEX schools_ru_idx ON schools "
                                  u"USING GIN(to_tsvector('russian', title));")
    yield momoko.Op(conn.execute, u"CREATE INDEX schools_en_idx ON schools "
                                  u"USING GIN(to_tsvector('english', title));")