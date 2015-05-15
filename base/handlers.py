# -*- coding: utf-8 -*-

import logging
from tornado import web, gen
from scientist.models import Scientist


__author__ = 'oks'


def base_request(function):
    def wrapper(*args, **kwargs):
        response_data = dict()
        try:
            data = function(*args, **kwargs)
            response_data.update(data)
        except Exception, ex:
            logging.exception(ex)
        return response_data
    return wrapper


class BaseRequestHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.application = None
        super(BaseRequestHandler, self).__init__(*args, **kwargs)
        self.payload = dict()
        self.current_user_id = self.get_secure_cookie(u'scientist')

    @gen.coroutine
    def get_current_user(self):
        user = None
        if self.current_user_id:
            user = yield Scientist.get_by_id(self.current_user_id)
        raise gen.Return(user)

    @gen.coroutine
    @base_request
    def get_response(self, data):
        return data

    def prepare(self):
        x = self.xsrf_token
        if not x:
            self.xsrf_token()