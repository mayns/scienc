# -*- coding: utf-8 -*-

import json
import datetime
import globals

__author__ = 'mayns'


class FieldDescriptor(object):

    __slots__ = ['store', 'restore', 'to_json', 'from_json', 'type', 'db_type',
                 'default', 'db_default', 'db_references', 'required', 'length', 'is_composite', 'primary_key']

    def __init__(self, store=None, restore=None, to_json=None, from_json=None, type=type, db_type=None, default=None,
                 db_default=None, db_references=None, required=False, length=None, is_composite=False, primary_key=False):

        self.store = store
        self.restore = restore
        self.to_json = to_json
        self.from_json = from_json
        self.type = type
        self.db_type = db_type
        self.default = default
        self.db_default = db_default
        self.db_references = db_references
        self.required = required
        self.length = length
        self.is_composite = is_composite
        self.primary_key = primary_key


class Text(FieldDescriptor):

    def __init__(self, default=None, db_type=None, **kwargs):
        """:rtype: unicode"""
        super(Text, self).__init__(default=default, db_type=db_type, **kwargs)

        self.type = basestring
        self.db_type = db_type or 'text'
        self.default = default or u''


class TSvector(FieldDescriptor):

    def __init__(self, db_type=None, **kwargs):
        """:rtype: unicode"""
        super(TSvector, self).__init__(db_type=db_type, **kwargs)
        self.db_type = 'tsvector'


class Array(FieldDescriptor):

    def __init__(self, default=None, db_type=None, **kwargs):
        """:rtype: list"""
        super(Array, self).__init__(default=default, db_type=db_type, **kwargs)
        self.db_type = db_type or 'text[]'
        self.store = lambda x: json.dumps(x).replace(u'[', u'{').replace(u']', u'}').replace(u'{{', u'[{').replace(u'}}', u'}]') \
            if self.db_type != 'text[]' else '{' + ', '.join(x) + '}'
        self.restore = json.loads if self.db_type != 'text[]' else None
        self.type = list
        self.default = default or []


class JsonObject(FieldDescriptor):

    def __init__(self, default=None, db_type=None, **kwargs):
        """:rtype: dict"""
        super(JsonObject, self).__init__(default=default, db_type=db_type, **kwargs)

        self.store = json.dumps
        self.restore = json.loads
        self.type = dict
        self.db_type = db_type or 'jsonb'
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

        self.store = lambda value: '1' if value else '0'
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

    def __init__(self, default=None, db_default=None, db_type=None, **kwargs):
        """:rtype: datetime"""
        super(Datetime, self).__init__(default=default, db_default=db_default, db_type=db_type, **kwargs)
        self.db_default = db_default or 'NULL'

        self.store = lambda value: value.strftime(globals.DATETIME_FORMAT[db_type]['DB']) \
            if (value and not isinstance(value, basestring)) else value or self.db_default

        self.to_json = lambda value: value.strftime(globals.DATETIME_FORMAT[db_type]['DB']) \
            if value and not isinstance(value, basestring) else value
        self.restore = lambda value: datetime.datetime.strptime(value, globals.DATETIME_FORMAT[db_type]['DB']) \
            if value else u''
        self.from_json = lambda value: \
            datetime.datetime.strptime(value, globals.DATETIME_FORMAT[db_type]['DB']).date() if value else u''
        self.type = datetime.date
        self.db_type = db_type or 'timestamp'
        self.default = default or None