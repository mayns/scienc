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

    @gen.coroutine
    def get_current_user(self):
        from scientist.scientist_bl import ScientistBL
        scientist_id = self.get_secure_cookie(u'scientist')
        print u'CURRENT USER!!!', scientist_id, type(scientist_id)
        if not scientist_id or scientist_id is None:
            return
        scientist = yield ScientistBL.get_scientist(scientist_id)
        raise gen.Return(scientist)

    @gen.coroutine
    @base_request
    def get_response(self, data):
        return data