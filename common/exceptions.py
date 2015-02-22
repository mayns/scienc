# -*- coding: utf-8 -*-


__author__ = 'oks'


class UserExistException(Exception):

    def __init__(self, login):
        self.message = u'Error: User with email {} already exists. Please log in'.format(login)