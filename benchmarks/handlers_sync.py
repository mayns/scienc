# -*- coding: utf-8 -*-

import logging
import settings
from tornado import web
import psycopg2
from common.utils import generate_id

FIELDS = lambda: ', '.join(['id', 'title', 'research_fields', 'description_short'])


__author__ = 'mayns'


class ProjectsHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.application = None
        super(ProjectsHandler, self).__init__(*args, **kwargs)
        self.payload = dict()

    def get(self, *args, **kwargs):
        logging.info(u'Sync GET')
        pass

    def post(self, *args, **kwargs):
        logging.info(u'Sync POST')
        title = self.get_argument(u'title', u'')
        research_fields = self.get_argument(u'research_fields', u'')
        description_short = self.get_argument(u'description_short', u'')
        self.add_to_db(title, research_fields, description_short)

    @property
    def conn(self):
        if not hasattr(self.application, 'conn'):
            self.application.conn = psycopg2.connect(**settings.SCIENCE_DB_TEST_MAP[u'NO_SHARD'])
        return self.application.conn

    @property
    def conn_shard(self):
        if not hasattr(self.application, 'conn_shard'):
            self.application.conn_shard = psycopg2.connect(**settings.SCIENCE_DB_TEST_MAP[u'SHARD'])
        return self.application.conn_shard

    def get_from_db(self):
        pass

    def add_to_db(self, title, research_fields, description_short):
        id = generate_id(17)
        vals = "{}, {}, {}, {}".format(id, title, research_fields.replace('[', '{').replace(']', '}'), description_short)
        sql_query = "INSERT INTO {tbl} ({fields}) VALUES ({vals})".format(tbl='projects_test',
                                                                          fields=FIELDS(),
                                                                          vals=vals)
        print sql_query
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        # self.conn.commit()