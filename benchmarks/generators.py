# -*- coding: utf-8 -*-

import random
import fauxfactory
from db.orm import MODELS
from common.utils import zip_values
from scientist.models import Scientist
from project.models import Project
import datetime
import environment

__author__ = 'mayns'


def generate_users(n=10):

    users = []
    create_fields = dict(zip_values(Scientist.CREATE_FIELDS, MODELS[Scientist.TABLE], empty_fields=1))

    for user in xrange(n):
        user_dict = {}
        for key, value in create_fields.iteritems():
            if value.type == basestring:
                if key == u'email':
                    user_dict[key] = fauxfactory.gen_email()
                else:
                    user_dict[key] = fauxfactory.gen_cyrillic(value.length)

            if value.type == datetime.date:
                user_dict[key] = fauxfactory.gen_date()

            if value.type == dict:
                if key == u'location':
                    user_dict[key] = dict(
                        country=fauxfactory.gen_cyrillic(),
                        city=fauxfactory.gen_cyrillic()
                    )
                if key == u'middle_education':
                    user_dict[key] = dict(
                        country=fauxfactory.gen_cyrillic(),
                        city=fauxfactory.gen_cyrillic(),
                        school=fauxfactory.gen_cyrillic(),
                        graduation_year=fauxfactory.gen_integer(min_value=1900, max_value=2020),
                    )

            if value.type == list:
                values = []
                if value.db_type == 'text[]':
                    for i in xrange(random.randint(1, 10)):
                        values.append(fauxfactory.gen_cyrillic())

                if value.db_type == 'bigint[]':
                    for i in xrange(random.randint(1, 10)):
                        values.append(fauxfactory.gen_integer(min_value=1, max_value=n))

                if value.db_type == 'json':
                    for i in xrange(random.randint(1, 5)):
                        value_json = {}
                        if key == u'high_education':
                            value_json[u'country'] = fauxfactory.gen_cyrillic()
                            value_json[u'city'] = fauxfactory.gen_cyrillic()
                            value_json[u'university'] = fauxfactory.gen_cyrillic(length=20)
                            value_json[u'faculty'] = fauxfactory.gen_cyrillic(length=20)
                            value_json[u'chair'] = fauxfactory.gen_cyrillic(length=20)
                            value_json[u'degree'] = fauxfactory.gen_cyrillic(length=10)
                            value_json[u'graduation_year'] = fauxfactory.gen_integer(min_value=1900, max_value=2020)

                        if key == u'publications':
                            value_json[u'id'] = fauxfactory.gen_integer()
                            value_json[u'title'] = fauxfactory.gen_cyrillic(length=100)
                            value_json[u'source'] = fauxfactory.gen_cyrillic(length=20)
                            value_json[u'year'] = fauxfactory.gen_integer(min_value=1900, max_value=2015)
                            value_json[u'link'] = fauxfactory.gen_url()

                        if key == u'contacts':
                            value_json[u'connection'] = random.choice(environment.CONTACT_TYPES)
                            value_json[u'number'] = fauxfactory.gen_alphanumeric()

                        values.append(value_json)
                user_dict[key] = values

        user_dict.update(pwd=fauxfactory.gen_alpha())

        users.append(user_dict)

    return users


def generate_projects(n=10):
    projects = []
    create_fields = dict(zip_values(Project.CREATE_FIELDS, MODELS[Project.TABLE], empty_fields=1))
