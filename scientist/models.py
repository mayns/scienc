# -*- coding: utf-8 -*-

from tornado import gen
from base.models import PSQLModel

__author__ = 'oks'


class Scientist(PSQLModel):

    TABLE = u'scientists'

    OVERVIEW_FIELDS = [u'id', u'first_name', u'middle_name', u'last_name', u'image_url',
                       u'participating_projects', u'location']

    EDITABLE_FIELDS = [u'first_name', u'middle_name', u'last_name', u'dob', u'gender',
                       u'image_url', u'location', u'middle_education', u'high_education',
                       u'publications', u'interests', u'about', u'contacts']

    SYSTEM_INFO = [u'dt_created']