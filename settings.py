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


# -------- STATIC ---------- #

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, u"templates"),
)

STATIC_PATH = os.path.join(PROJECT_PATH, u"static")

# JINJA_FILTERS = (
#     u'jinja.filters',
# )
#
# JINJA_EXTS = (
#     u'jinja2.ext.i18n',
# )

BABEL_CONF = u'babel.cfg'


# -------- REDIS ---------- #

REDIS_PARTITION = u'Science'

REDIS_PARTITION_MAP = {
    REDIS_PARTITION: dict(
        master={u"host": u"localhost", u"port": 6390, u"db": 0}
    ),
}
REDIS_MAX_CONNECTIONS = 50000

PSQL_ROOT_USER = u'postgres'
PSQL_ROOT_PASSWORD = u'postgres'

SCIENCE_DB = dict(
    database=u'science_db',
    host=u'localhost',
    port=5432,
    user=PSQL_ROOT_USER,
    password=PSQL_ROOT_PASSWORD,
)

PSQL_MIN_CONNECTIONS = 1
PSQL_MAX_CONNECTIONS = 100