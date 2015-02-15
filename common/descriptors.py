# -*- coding: utf-8 -*-

import json
import datetime
import environment

__author__ = 'mayns'

# TODO: -----------------------
# column_values = map(lambda x: (x[0], json.dumps(x[1]).replace(u'[', u'{').replace(u']', u'}').
# replace(u'{{', u'[{').replace(u'}}', u'}]'))
# if type(x[1]) in [list, dict, int, long] else x, column_values)
# -----------------------------


class FieldDescriptor(object):

    __slots__ = ['store', 'restore', 'type', 'db_type', 'validator', 'default', 'required']

    def __init__(self, store=None, restore=None, validator=None, default=None, required=False):

        self.store = store
        self.restore = restore
        self.type = None
        self.db_type = None
        self.validator = validator
        self.default = default
        self.required = required


class Text(FieldDescriptor):

    def __init__(self, default=None, **kwargs):
        """:rtype: unicode"""
        super(Text, self).__init__(default=default, **kwargs)

        self.type = basestring
        self.db_type = 'text'
        self.default = default or u''


class JsonArray(FieldDescriptor):

    def __init__(self, default=None, **kwargs):
        """:rtype: list"""
        super(JsonArray, self).__init__(default=default, **kwargs)

        self.store = json.dumps
        self.restore = json.loads
        self.type = list
        self.db_type = 'text[]'
        self.default = default or []


class JsonObject(FieldDescriptor):

    def __init__(self, default=None, **kwargs):
        """:rtype: dict"""
        super(JsonObject, self).__init__(default=default, **kwargs)

        self.store = json.dumps
        self.restore = json.loads
        self.type = dict
        self.db_type = 'json'
        self.default = default or {}


class JsonSet(FieldDescriptor):

    def __init__(self, default=None, **kwargs):
        """:rtype: set"""
        super(JsonSet, self).__init__(default=default, **kwargs)

        self.store = lambda i: json.dumps(list(i))
        self.restore = lambda i: set(json.loads(i))
        self.type = set
        self.db_type = 'text[]'
        self.default = default or set()


class Boolean(FieldDescriptor):

    def __init__(self, default=None, **kwargs):
        """:rtype: Boolean"""
        super(Boolean, self).__init__(default=default, **kwargs)

        self.store = lambda value: u'1' if value else u''
        self.restore = bool
        self.type = bool
        self.db_type = 'boolean'
        self.default = default or False


class Integer(FieldDescriptor):

    def __init__(self, default=None, **kwargs):
        """:rtype: int"""
        super(Integer, self).__init__(default=default, **kwargs)

        self.restore = int
        self.type = int
        self.db_type = 'bigint'
        self.default = default or 0


class ID(FieldDescriptor):

    def __init__(self, default=None, **kwargs):
        """:rtype: int"""
        super(ID, self).__init__(default=default, **kwargs)

        self.restore = int
        self.type = int
        self.db_type = 'bigserial'
        self.default = default or 0


class Float(FieldDescriptor):

    def __init__(self, default=None, **kwargs):
        """:rtype: float"""
        super(Float, self).__init__(default=default, **kwargs)

        self.restore = float
        self.type = float
        self.db_type = 'real'
        self.default = default or 0.0


class Datetime(FieldDescriptor):

    def __init__(self, default=None, **kwargs):
        """:rtype: datetime"""
        super(Datetime, self).__init__(default=default, **kwargs)

        self.store = lambda value: value.strftime(environment.TIMESTAMP_FORMAT) if value else u''
        self.restore = lambda value: datetime.datetime.strptime(value, environment.TIMESTAMP_FORMAT) if value else u''
        self.type = datetime.date
        self.db_type = 'timestamp'
        self.default = default or u''