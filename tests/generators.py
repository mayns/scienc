# -*- coding: utf-8 -*-

import random
import fauxfactory
from db.orm import MODELS
from common.utils import zip_values
from scientist.models import Scientist
import datetime

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
                pass

            if value.type == list:
                pass

        user_dict.update(pwd=fauxfactory.gen_alpha())

        users.append(user_dict)

    return users