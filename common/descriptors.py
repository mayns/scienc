# -*- coding: utf-8 -*-

import json
import datetime
import environment

__author__ = 'mayns'


class FieldDescriptor(object):

    __slots__ = ['store', 'restore', 'to_json', 'type', 'db_type', 'default', 'db_default', 'db_references', 'required']

    def __init__(self, store=None, restore=None, to_json=None, type=type, db_type=None, default=None,
                 db_default=None, db_references=None, required=False):

        self.store = store
        self.restore = restore
        self.to_json = to_json
        self.type = type
        self.db_type = db_type
        self.default = default
        self.db_default = db_default
        self.db_references = db_references
        self.required = required


class Text(FieldDescriptor):

    def __init__(self, default=None, db_type=None, **kwargs):
        """:rtype: unicode"""
        super(Text, self).__init__(default=default, db_type=db_type, **kwargs)

        self.type = basestring
        self.db_type = db_type or 'text'
        self.default = default or u''


class JsonArray(FieldDescriptor):

    def __init__(self, default=None, db_type=None, **kwargs):
        """:rtype: list"""
        super(JsonArray, self).__init__(default=default, db_type=db_type, **kwargs)
        self.store = lambda x: json.dumps(x).replace(u'[', u'{').replace(u']', u'}').replace(u'{{', u'[{').replace(u'}}', u'}]').replace('\'', '\"')
        self.restore = json.loads
        self.type = list
        self.db_type = db_type or 'text[]'
        self.default = default or []


class JsonObject(FieldDescriptor):

    def __init__(self, default=None, db_type=None, **kwargs):
        """:rtype: dict"""
        super(JsonObject, self).__init__(default=default, db_type=db_type, **kwargs)

        self.store = json.dumps
        self.restore = json.loads
        self.type = dict
        self.db_type = db_type or 'json'
        self.default = default or {}


class JsonSet(FieldDescriptor):

    def __init__(self, default=None, db_type=None, **kwargs):
        """:rtype: set"""
        super(JsonSet, self).__init__(default=default, db_type=db_type, **kwargs)

        self.store = lambda i: json.dumps(list(i))
        self.restore = lambda i: set(json.loads(i))
        self.type = set
        self.db_type = db_type or 'text[]'
        self.default = default or set()


class Boolean(FieldDescriptor):

    def __init__(self, default=None, db_type=None, **kwargs):
        """:rtype: Boolean"""
        super(Boolean, self).__init__(default=default, db_type=db_type, **kwargs)

        self.store = lambda value: u'1' if value else u''
        self.restore = bool
        self.type = bool
        self.db_type = db_type or 'boolean'
        self.default = default or False


class Integer(FieldDescriptor):

    def __init__(self, default=None, db_type=None, **kwargs):
        """:rtype: int"""
        super(Integer, self).__init__(default=default, db_type=db_type, **kwargs)

        self.store = str
        self.restore = int
        self.type = int
        self.db_type = db_type or 'bigint'
        self.default = default or 0


class ID(FieldDescriptor):

    def __init__(self, default=None, db_type=None, **kwargs):
        """:rtype: int"""
        super(ID, self).__init__(default=default, db_type=db_type, **kwargs)

        self.store = str
        self.restore = int
        self.type = int
        self.db_type = db_type or 'bigserial'
        self.default = default or 0


class Float(FieldDescriptor):

    def __init__(self, default=None, db_type=None, **kwargs):
        """:rtype: float"""
        super(Float, self).__init__(default=default, db_type=db_type, **kwargs)

        self.restore = float
        self.type = float
        self.db_type = db_type or 'real'
        self.default = default or 0.0


class Datetime(FieldDescriptor):

    def __init__(self, default=None, db_type=None, **kwargs):
        """:rtype: datetime"""
        super(Datetime, self).__init__(default=default, db_type=db_type, **kwargs)

        self.store = lambda value: value.strftime(environment.DATETIME_FORMAT[db_type]['DB']) \
            if value and not isinstance(value, basestring) else value
        self.to_json = lambda value: value.strftime(environment.DATETIME_FORMAT[db_type]['HUMAN']) \
            if value and not isinstance(value, basestring) else value
        self.restore = lambda value: datetime.datetime.strptime(value, environment.DATETIME_FORMAT[db_type]['HUMAN']) \
            if value else u''
        self.type = datetime.date
        self.db_type = db_type or 'timestamp'
        self.default = default or u''