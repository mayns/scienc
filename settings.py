# -*- coding: utf-8 -*-

import os
import socket

__author__ = 'oks'


DEVELOPMENT = False


# -------- PROJECT MAIN ---------- #

PROJECT_TITLE = u'ScienceMates'
SERVER_IP = u'localhost'
PROJECT_PATH = os.path.join(os.path.dirname(__file__))

STATIC_PATH = os.path.dirname(__file__)
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), u'stands/templates')

COOKIE_SECRET = unicode(hash(u"Alice was beginning to get very tired of sitting by her sister on the bank"))
SESSION_SECRET = unicode(hash(u"However, this bottle was not marked `poison,' so Alice ventured to taste it"))


# -------- MEDIA SERVER ---------- #

MEDIA_SERVER_HOST = u'media-science.dev:9190'


# --------- POSTGRESQL ----------- #

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