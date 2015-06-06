# -*- coding: utf-8 -*-

from db.orm import *

__author__ = 'mayns'


TABLES = dict(
    projects={
        u'title': Text(length=100),
        u'description_short': Text(length=300),
        u'research_fields': Array(),
    },
)