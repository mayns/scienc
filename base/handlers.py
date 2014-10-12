# -*- coding: utf-8 -*-

from tornado import web, gen

__author__ = 'oks'


def base_request(function):
    def wrapper(*args, **kwargs):
        from base.ajax_data import AJAX_STATUS_SUCCESS, AJAX_STATUS_ERROR
        response_data = dict(
            status=AJAX_STATUS_ERROR
        )
        try:
            data = function(*args, **kwargs)
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
        super(BaseRequestHandler, self).__init__(*args, **kwargs)

    def get_current_user(self):
        return self.get_secure_cookie(u"scientist")

    @gen.coroutine
    @base_request
    def get_response(self, data):
        return data

    # def get_payload(self):
    #     # must be implemented in child class
    #     raise NotImplementedError


class LoginHandler(BaseRequestHandler):
    def post(self):
        self.set_secure_cookie(u'scientist', self.get_argument(u'name'))
        self.finish()