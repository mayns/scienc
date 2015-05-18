# -*- coding: utf-8 -*-

import logging
import settings
from tornado import web
import psycopg2


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
        pass

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

    def get_from_db(self, conn):
        pass