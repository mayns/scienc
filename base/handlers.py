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
        return self.get_secure_cookie("user")

    def get(self, *args, **kwargs):
        if not self.current_user:
            self.redirect("/login")
            return
        if not self.get_secure_cookie(u"science_mates_cookie"):
            self.set_secure_cookie(u"science_mates_cookie", "myvalue")
        return self.get_secure_cookie(u"science_mates_cookie")

    @gen.coroutine
    @base_request
    def get_response(self, data):
        return data