# -*- coding: utf-8 -*-


__author__ = 'oks'


class UserExistException(Exception):

    def __init__(self, login):
        self.message = u'Error: User with email {} already exists. Please log in'.format(login)
        super(UserExistException, self).__init__(self.message)


class InvalidData(Exception):

    def __init__(self, field):
        self.message = u'Invalid Data received for {field}'.format(field=field)
        super(InvalidData, self).__init__(self.message)


class RequiredFields(Exception):

    def __init__(self, fields):
        if isinstance(fields, list):
            self.message = u'These fields are required: {}'.format(u', '.join(fields))
        if isinstance(fields, basestring):
            self.message = u'This field is required: {field}'.format(field=fields)
        super(RequiredFields, self).__init__(self.message)


class PSQLException(Exception):

    def __init__(self, msg):
        self.message = u'PSQL Exception: {}'.format(msg)
        super(PSQLException, self).__init__(self.message)
