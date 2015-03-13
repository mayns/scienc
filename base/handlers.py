# -*- coding: utf-8 -*-

from tornado import web, gen
from scientist.models import Scientist

__author__ = 'oks'


def base_request(function):
    def wrapper(*args, **kwargs):
        from base.ajax_data import AJAX_STATUS_SUCCESS, AJAX_STATUS_ERROR
        response_data = dict(
            status=AJAX_STATUS_ERROR
        )
        try:
            data = function(*args, **kwargs)
            if u'message' not in data:
                response_data = dict(
                    status=AJAX_STATUS_SUCCESS
                )
            response_data.update(dict(data=data))
        except Exception, ex:
            print ex
        return response_data
    return wrapper


class BaseRequestHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.payload = dict()
        self.current_user_id = self.get_secure_cookie(u'scientist')
        super(BaseRequestHandler, self).__init__(*args, **kwargs)

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