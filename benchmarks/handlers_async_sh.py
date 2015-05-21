# -*- coding: utf-8 -*-

import logging
import settings
from tornado import web, gen
import json
import globals
import momoko
from db.connections import PSQLClient
from common.utils import generate_id

fields = ['id', 'title', 'research_fields', 'description_short']

FIELDS = lambda: ', '.join(fields)


__author__ = 'mayns'


class UserHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):

        scientist_data = dict(
            id='',
            image_url='',
            liked_projects='',
            desired_vacancies='',
            managing_project_ids=''
        )
        self.finish(json.dumps(scientist_data))


class ProjectsHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.application = None
        super(ProjectsHandler, self).__init__(*args, **kwargs)
        self.payload = dict()

    @gen.coroutine
    def get(self, *args, **kwargs):
        logging.info(u'Async GET')
        projects = yield self.get_from_db()
        for project in projects:
            project.update(research_fields=
                           [dict(id=f, name=globals.SCIENCE_FIELDS_MAP[f]) for f in project[u'research_fields']
                                if f in globals.SCIENCE_FIELDS_MAP])
        self.finish(dict(data=projects))

    @gen.coroutine
    def post(self, *args, **kwargs):
        logging.info(u'Async POST')
        title = self.get_argument(u'title', u'')
        research_fields = self.get_argument(u'research_fields', u'')
        description_short = self.get_argument(u'description_short', u'')
        yield self.add_to_db(title, research_fields, description_short)

    @property
    def conn(self):
        if not hasattr(self.application, 'conn'):
            self.application.conn = \
                PSQLClient.get_client(dsn=u'dbname={database} user={user} password={password} host={host} '
                                          u'port={port}'.format(**settings.SCIENCE_DB_TEST_MAP[u'SHARD']))
        return self.application.conn

    @gen.coroutine
    def get_from_db(self):
        sql_query = "SELECT {fields} FROM {tbl}".format(fields=FIELDS(), tbl='projects')
        sql_string = "SELECT get_query('{q}'::text);".format(q=sql_query)
        cursor = yield momoko.Op(self.conn.execute, sql_string)
        res = cursor.fetchall()
        raise gen.Return([dict(zip(fields, r)) for r in res])

    @gen.coroutine
    def add_to_db(self, title, research_fields, description_short):
        _id = generate_id(21)
        vals = "''{}'', ''{}'', ''{}'', ''{}''".format(_id, title,
                                               research_fields.replace('[', '{').replace(']', '}'), description_short)
        sql_query = "INSERT INTO {tbl} ({fields}) VALUES ({vals})".format(tbl='projects',
                                                                          fields=FIELDS(),
                                                                          vals=vals)
        sql_string = "SELECT execute_query('{q_id}'::text, '{q}'::text);".format(q_id=_id, q=sql_query)
        logging.info('SQL: {}'.format(sql_string))
        try:
            yield momoko.Op(self.conn.execute, sql_string)

        except Exception, ex:
            logging.exception(ex)