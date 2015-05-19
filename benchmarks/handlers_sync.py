# -*- coding: utf-8 -*-

import logging
import settings
from tornado import web
import psycopg2
import json
import globals
from common.utils import generate_id

fields = ['id', 'title', 'research_fields', 'description_short']

FIELDS = lambda: ', '.join(fields)


__author__ = 'mayns'


class UserHandler(web.RequestHandler):
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

    def get(self, *args, **kwargs):
        logging.info(u'Sync GET')
        projects = self.get_from_db()
        for project in projects:
            project.update(research_fields=
                           [dict(id=f, name=globals.SCIENCE_FIELDS_MAP[f]) for f in project[u'research_fields']
                                if f in globals.SCIENCE_FIELDS_MAP])
        self.finish(dict(data=projects))

    def post(self, *args, **kwargs):
        logging.info(u'Sync POST')
        logging.info(args)
        logging.info(kwargs)
        title = self.get_argument(u'title', u'')
        logging.info(title)
        research_fields = self.get_argument(u'research_fields', u'')
        description_short = self.get_argument(u'description_short', u'')
        self.add_to_db(title, research_fields, description_short)

    @property
    def conn(self):
        if not hasattr(self.application, 'conn'):
            self.application.conn = psycopg2.connect(**settings.SCIENCE_DB_TEST_MAP[u'NO_SHARD_S'])
        return self.application.conn

    @property
    def conn_shard(self):
        if not hasattr(self.application, 'conn_shard'):
            self.application.conn_shard = psycopg2.connect(**settings.SCIENCE_DB_TEST_MAP[u'SHARD'])
        return self.application.conn_shard

    def get_from_db(self):
        sql_query = "SELECT {fields} FROM {tbl}".format(fields=FIELDS(), tbl='projects')
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        res = cursor.fetchall()
        return [dict(zip(fields, r)) for r in res]

    def add_to_db(self, title, research_fields, description_short):
        _id = generate_id(21)
        vals = "'{}', '{}', '{}', '{}'".format(_id, title,
                                               research_fields.replace('[', '{').replace(']', '}'), description_short)
        sql_query = "INSERT INTO {tbl} ({fields}) VALUES ({vals})".format(tbl='projects',
                                                                          fields=FIELDS(),
                                                                          vals=vals)
        logging.info('SQL: {}'.format(sql_query))
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_query)
            self.conn.commit()
        except Exception, ex:
            logging.exception(ex)