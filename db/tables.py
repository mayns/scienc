# -*- coding: utf-8 -*-

from common.descriptors import *

__author__ = 'mayns'


TABLES = dict(

    countries = {
        u'id': ID(db_type='smallserial'),
        u'title_en': Text(),
        u'title_ru': Text(),
    },

    cities = {
        u'id': ID(),
        u'country_id': Integer(db_type='smallint', db_references='countries(id)'),
        u'region': Text(db_default='NULL'),
        u'area': Text(db_default='NULL'),
        u'title': Text(),
    },

    main_cities = {
        u'id': ID(db_type='smallserial'),
        u'country_id': Integer(db_type='smallint', db_references='countries(id)'),
        u'city_id': Integer(db_references='cities(id)'),
        u'title': Text(),
    },

    universities = {
        u'id': ID(),
        u'city_id': Integer(db_references='cities(id)'),
        u'title': Text(),
    },

    faculties = {
        u'id': ID(),
        u'university_id': Integer(db_references='universities(id)'),
        u'title': Text(),
    },

    chairs = {
        u'id': ID(),
        u'faculty_id': Integer(db_references='faculties(id)'),
        u'title': Text(),
    },

    schools = {
        u'id': ID(),
        u'city_id': Integer(db_references='cities(id)'),
        u'title': Text(),
    },
)