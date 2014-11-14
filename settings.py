# -*- coding: utf-8 -*-

import os

__author__ = 'oks'


# -------- PROJECT MAIN ---------- #

PROJECT_ID = u'ScienceMates'
PROJECT_NAME = u'ScienceMates'
PROJECT_TITLE = u'ScienceMates'
SERVER_IP = u'localhost'
PROJECT_PATH = os.path.join(os.path.dirname(__file__))

COOKIE_SECRET = u"wfgelwdhgw734862ihdi"
SESSION_SECRET = u"tf7843dyjbhxhswydwihdidhwq"


# -------- POSTGRESQL ---------- #

PSQL_ROOT_USER = u'postgres'
PSQL_ROOT_PASSWORD = u'postgres'

SCIENCE_DB = dict(
    database=u'science',
    host=u'localhost',
    port=5432,
    user=PSQL_ROOT_USER,
    password=PSQL_ROOT_PASSWORD,
)

PSQL_MIN_CONNECTIONS = 1
PSQL_MAX_CONNECTIONS = 100