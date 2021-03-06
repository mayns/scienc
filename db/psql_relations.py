# -*- coding: utf-8 -*-

from tornado import gen
import copy

import settings
from common.descriptors import *
from db.connections import PSQLClient
from db.orm import MODELS
from db.tables import TABLES

import psycopg2
import momoko

__author__ = 'mayns'


ALL_TABLES = copy.deepcopy(MODELS)
ALL_TABLES.update(TABLES)


def create_db():
    from psycopg2 import connect
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    dbs_param = settings.SCIENCE_DB
    root_con = connect(dbname=u'postgres', user=settings.PSQL_ROOT_USER, host=dbs_param[u'host'],
                       port=dbs_param[u'port'], password=settings.PSQL_ROOT_PASSWORD)
    root_con.set_client_encoding('UTF-8')
    root_cursor = root_con.cursor()
    root_cursor.execute(u"SELECT 1 FROM pg_roles WHERE rolname='{}'".format(dbs_param[u'user']))
    exist_user = root_cursor.fetchone()
    if not exist_user:
        root_cursor.execute(u'CREATE USER {}'.format(dbs_param[u'user']))
    root_cursor.execute(u"ALTER USER {} WITH PASSWORD '{}'".format(dbs_param[u'user'], dbs_param[u'password']))
    root_cursor.execute(u'ALTER USER {} CREATEDB'.format(dbs_param[u'user']))
    root_con.commit()
    root_con.close()

    con = connect(dbname=u'postgres', user=dbs_param[u'user'], host=dbs_param[u'host'],
                  port=dbs_param[u'port'], password=dbs_param[u'password'])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()
    cursor.execute(u"SELECT 1 FROM pg_database WHERE datname='{}'".format(dbs_param[u'database']))
    exist_db = cursor.fetchone()
    if exist_db:
        cursor.execute(u'DROP database {};'.format(dbs_param[u'database']))
    cursor.execute(u'CREATE DATABASE {}'.format(dbs_param[u'database']))
    con.commit()
    con.close()


@gen.coroutine
def create_config():
    conn = PSQLClient.get_client()
    try:
        yield momoko.Op(conn.execute, u"""
        CREATE TEXT SEARCH DICTIONARY russian_ispell (
        TEMPLATE = ispell,
        DictFile = russian,
        AffFile = russian,
        StopWords = russian
        );

        CREATE TEXT SEARCH DICTIONARY english_ispell (
        TEMPLATE = ispell,
        DictFile = english,
        AffFile = english,
        StopWords = english
        );

        CREATE TEXT SEARCH CONFIGURATION international ( COPY = russian );

        ALTER TEXT SEARCH CONFIGURATION international ALTER MAPPING FOR hword, hword_part, word WITH russian_ispell, russian_stem;
        ALTER TEXT SEARCH CONFIGURATION international ALTER MAPPING FOR asciihword, asciiword, hword_asciipart WITH english_ispell, english_stem;
        """)

        print 'configuration for text search has been created'
    except (psycopg2.Warning, psycopg2.Error) as error:
        raise Exception(str(error))


@gen.coroutine
def create_relations():
    try:
        yield delete_tables()
        yield create_relation_roles()
        yield create_relation_scientists()
        yield create_relation_projects()
        yield create_relation_participants()
        yield create_relation_vacancies()
        yield create_relation_responses()
        yield create_relation_countries()
        yield create_relation_cities()
        yield create_relation_main_cities()
        yield create_relation_universities()
        yield create_relation_faculties()
        yield create_relation_chairs()
        yield create_relation_schools()
        print u'done'

    except (psycopg2.Warning, psycopg2.Error) as error:
        raise Exception(str(error))


@gen.coroutine
def delete_tables():
    conn = PSQLClient.get_client()
    tables = ALL_TABLES.keys()
    for table in tables:
        try:
            print u'deleting {}'.format(table)
            yield momoko.Op(conn.execute, u'DROP TABLE %s CASCADE' % table)
        except Exception, ex:
            print ex
            continue


def prepare_creation(table):
    query_table = ''
    composite_key = []
    for k, v in ALL_TABLES[table].iteritems():
        query_table += k
        query_table += ' '
        query_table += v.db_type
        if isinstance(v, ID) or v.primary_key:
            query_table += ' primary key'
        if v.db_references:
            query_table += ' REFERENCES %s ON DELETE CASCADE' % v.db_references
        if v.db_default:
            query_table += ' DEFAULT %s' % v.db_default
        if v.is_composite:
            composite_key.append(k)
        query_table += ', '
    query_table = query_table[:-2]
    if composite_key:
        return """CREATE TABLE {table} ({query}, PRIMARY KEY({key}));""".format(table=table, query=query_table,
                                                                                key=','.join(composite_key))
    return """CREATE TABLE {table} ({query});""".format(table=table, query=query_table)


@gen.coroutine
def create_relation_scientists():
    table = u'scientists'
    print u'creating {} relation'.format(table)
    conn = PSQLClient.get_client()
    query = prepare_creation(table)
    yield momoko.Op(conn.execute, query)

    yield momoko.Op(conn.execute, u"CREATE INDEX scientists_first_name_idx ON scientists (first_name);")
    yield momoko.Op(conn.execute, u"CREATE INDEX scientists_last_name_idx ON scientists (last_name);")
    yield momoko.Op(conn.execute, u"CREATE INDEX scientists_middle_name_idx ON scientists (middle_name);")
    yield momoko.Op(conn.execute, u"CREATE INDEX scientists_interests_idx ON scientists USING GIN(interests);")


@gen.coroutine
def create_relation_participants():
    table = u'participants'
    print u'creating {} relation'.format(table)
    conn = PSQLClient.get_client()
    query = prepare_creation(table)
    yield momoko.Op(conn.execute, query)

    yield momoko.Op(conn.execute, u"CREATE INDEX participants_first_name_idx ON participants (first_name);")
    yield momoko.Op(conn.execute, u"CREATE INDEX participants_last_name_idx ON participants (last_name);")
    yield momoko.Op(conn.execute, u"CREATE INDEX participants_middle_name_idx ON participants (middle_name);")
    yield momoko.Op(conn.execute, u"CREATE INDEX participants_role_name_idx ON participants (role_name);")


@gen.coroutine
def create_relation_projects():
    table = u'projects'
    print u'creating {} relation'.format(table)
    conn = PSQLClient.get_client()
    query = prepare_creation(table)
    yield momoko.Op(conn.execute, query)

    # INDEXES:
    yield momoko.Op(conn.execute, u"UPDATE projects SET title_tsvector = (to_tsvector('international', title));")

    yield momoko.Op(conn.execute, u"UPDATE projects SET description_short_tsvector"
                                  u" = (to_tsvector('international', description_short));")

    yield momoko.Op(conn.execute, u"CREATE INDEX title_idx ON projects "
                                  u"USING GIN (title_tsvector);")

    yield momoko.Op(conn.execute, u"CREATE INDEX description_short_idx ON projects "
                                  u"USING GIN (description_short_tsvector);")

    yield momoko.Op(conn.execute, u"CREATE INDEX tags_idx ON projects(tags);")

    yield momoko.Op(conn.execute, u"""DROP FUNCTION IF EXISTS project_vector_update() CASCADE;""")

    yield momoko.Op(conn.execute, u"""DROP TRIGGER IF EXISTS tsvectorupdate on projects CASCADE;""")

    yield momoko.Op(conn.execute,
    u"""CREATE FUNCTION project_vector_update() RETURNS TRIGGER AS $$
        BEGIN
            IF TG_OP = 'INSERT' THEN
                new.title_tsvector = to_tsvector('international', COALESCE(NEW.title, ''));
                new.description_short_tsvector = to_tsvector('international', COALESCE(NEW.description_short, ''));

            END IF;
            IF TG_OP = 'UPDATE' THEN
                IF NEW.title <> OLD.title THEN
                    new.title_tsvector = to_tsvector('international', COALESCE(NEW.title, ''));
                END IF;
                IF NEW.description_short <> OLD.description_short THEN
                    new.description_short_tsvector = to_tsvector('international', COALESCE(NEW.description_short, ''));
                END IF;

            END IF;
            RETURN NEW;
        END
        $$ LANGUAGE 'plpgsql';""")

    yield momoko.Op(conn.execute, u"CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE "
                                  u"ON projects FOR EACH ROW EXECUTE PROCEDURE project_vector_update();")


@gen.coroutine
def create_relation_vacancies():
    table = u'vacancies'
    print u'creating {} relation'.format(table)
    conn = PSQLClient.get_client()
    query = prepare_creation(table)
    yield momoko.Op(conn.execute, query)

    yield momoko.Op(conn.execute, u"UPDATE vacancies SET vacancy_name_tsvector = (to_tsvector('international',"
                                  u"vacancy_name));")

    yield momoko.Op(conn.execute, u"UPDATE vacancies SET vacancy_description_tsvector"
                                  u" = (to_tsvector('international', description));")

    yield momoko.Op(conn.execute, u"CREATE INDEX vacancy_name_idx ON vacancies "
                                  u"USING GIN(vacancy_name_tsvector);")

    yield momoko.Op(conn.execute, u"CREATE INDEX vacancy_description_idx ON vacancies "
                                  u"USING GIN(vacancy_description_tsvector);")

    yield momoko.Op(conn.execute, u"""DROP FUNCTION IF EXISTS vacancy_vector_update() CASCADE;""")

    yield momoko.Op(conn.execute, u"""DROP TRIGGER IF EXISTS tsvectorupdate on vacancies CASCADE;""")

    yield momoko.Op(conn.execute,

    u"""CREATE FUNCTION vacancy_vector_update() RETURNS TRIGGER AS $$
    BEGIN
        IF TG_OP = 'INSERT' THEN
            new.vacancy_name_tsvector = to_tsvector('international', COALESCE(NEW.vacancy_name, ''));
            new.vacancy_description_tsvector = to_tsvector('international', COALESCE(NEW.description, ''));
        END IF;

        IF TG_OP = 'UPDATE' THEN

            IF NEW.vacancy_name <> OLD.vacancy_name THEN
                new.vacancy_name_tsvector = to_tsvector('international', COALESCE(NEW.vacancy_name, ''));
            END IF;

            IF NEW.description <> OLD.description THEN
                new.vacancy_description_tsvector = to_tsvector('international', COALESCE(NEW.description, ''));
            END IF;

        END IF;
        RETURN NEW;
    END
    $$ LANGUAGE 'plpgsql';""")

    yield momoko.Op(conn.execute, u"CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE "
                                  u"ON vacancies FOR EACH ROW EXECUTE PROCEDURE vacancy_vector_update();")


@gen.coroutine
def create_relation_responses():
    table = u'responses'
    print u'creating {} relation'.format(table)
    conn = PSQLClient.get_client()
    query = prepare_creation(table)
    yield momoko.Op(conn.execute, query)


@gen.coroutine
def create_relation_roles():
    table = u'roles'
    print u'creating {} relation'.format(table)
    conn = PSQLClient.get_client()
    query = prepare_creation(table)
    yield momoko.Op(conn.execute, query)


# ---------------------- LOCATION TABLES --------------------------

@gen.coroutine
def create_relation_countries():
    table = u'countries'
    print u'creating {} relation'.format(table)
    conn = PSQLClient.get_client()
    query = prepare_creation(table)
    yield momoko.Op(conn.execute, query)

    yield momoko.Op(conn.execute, u"CREATE INDEX countries_title_ru_idx ON countries (title_ru);")
    yield momoko.Op(conn.execute, u"CREATE INDEX countries_title_en_idx ON countries (title_en);")


@gen.coroutine
def create_relation_cities():
    table = u'cities'
    print u'creating {} relation'.format(table)
    conn = PSQLClient.get_client()
    query = prepare_creation(table)
    yield momoko.Op(conn.execute, query)

    yield momoko.Op(conn.execute, u"CREATE INDEX cities_region_idx ON cities (region);")
    yield momoko.Op(conn.execute, u"CREATE INDEX cities_area_idx ON cities (area);")
    yield momoko.Op(conn.execute, u"CREATE INDEX cities_title_idx ON cities (title);")



@gen.coroutine
def create_relation_main_cities():
    table = u'main_cities'
    print u'creating {} relation'.format(table)
    conn = PSQLClient.get_client()
    query = prepare_creation(table)
    yield momoko.Op(conn.execute, query)


# ---------------------- EDUCATION TABLES --------------------------

@gen.coroutine
def create_relation_universities():
    table = u'universities'
    print u'creating {} relation'.format(table)
    conn = PSQLClient.get_client()
    query = prepare_creation(table)
    yield momoko.Op(conn.execute, query)

    yield momoko.Op(conn.execute, u"CREATE INDEX universities_title_idx ON universities (title);")


@gen.coroutine
def create_relation_faculties():
    table = u'faculties'
    print u'creating {} relation'.format(table)
    conn = PSQLClient.get_client()
    query = prepare_creation(table)
    yield momoko.Op(conn.execute, query)

    yield momoko.Op(conn.execute, u"CREATE INDEX faculties_title_idx ON faculties (title);")


@gen.coroutine
def create_relation_chairs():
    table = u'chairs'
    print u'creating {} relation'.format(table)
    conn = PSQLClient.get_client()
    query = prepare_creation(table)
    yield momoko.Op(conn.execute, query)

    yield momoko.Op(conn.execute, u"CREATE INDEX chairs_title_idx ON chairs (title);")


@gen.coroutine
def create_relation_schools():
    table = u'schools'
    print u'creating {} relation'.format(table)
    conn = PSQLClient.get_client()
    query = prepare_creation(table)
    yield momoko.Op(conn.execute, query)

    yield momoko.Op(conn.execute, u"CREATE INDEX schools_title_idx ON schools (title);")
