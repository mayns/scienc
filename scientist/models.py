# -*- coding: utf-8 -*-

from tornado import gen
from base.models import PSQLModel

__author__ = 'oks'


class Scientist(PSQLModel):

    TABLE = u'scientists'

    OVERVIEW_FIELDS = [u'id', u'first_name', u'middle_name', u'last_name', u'image_url',
                       u'participating_projects', u'location']

    @classmethod
    @gen.coroutine
    def get_scientist(cls, scientist_id):
        # json_data = {}
        scientist_data = yield Scientist.get_json_by_id(scientist_id)
        if not scientist_data:
            raise gen.Return({})

        print scientist_data
        # json_data = dict(zip(Scientist.COLUMNS, scientist))
        raise gen.Return(scientist_data)

    @classmethod
    @gen.coroutine
    def get_all(cls):
        json_data = []
        try:
            scientists = yield Scientist.get_all_json(columns)
            if not scientists:
                raise gen.Return([])
            json_data = [dict(zip(columns, entity_data)) for entity_data in scientists]
            print json_data
            for j in json_data:
                j[u'id'] = int(j[u'id'])
                j[u'full_name'] = j.pop(u'first_name') + ' ' + j.pop(u'middle_name') + ' ' + j.pop(u'last_name')
                j[u'location'] = j.pop(u'location_city') + ', ' + j.pop(u'location_country')
                j[u'projects'] = len(j.pop(u'project_ids') or [])
        except Exception, ex:
            print u'Exception', ex
        raise gen.Return(json_data)