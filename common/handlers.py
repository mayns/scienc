# -*- coding: utf-8 -*-


from tornado import gen
from base.handlers import BaseRequestHandler

__author__ = 'oks'


# class HomeHandler(BaseRequestHandler):
#     @gen.coroutine
#     def get(self):
#         # self.render(u'index.html')
#         self.render(u'index.html')
#
#
# class NotFoundHandler(BaseRequestHandler):
#     @gen.coroutine
#     def get(self):
#         self.render(u'404.html')


class LoginHandler(BaseRequestHandler):

    @gen.coroutine
    def post(self):
        print u'login'
        from scientist.scientist_bl import ScientistBL
        # email = self.get_argument(u'email')
        # email = u'oksgorobets@gmail.com'
        email = u'qwe@qwe'
        # passw = self.get_argument(u'password')
        passw = 'qwe'
        scientist_id = yield ScientistBL.check_scientist(email, passw)
        self.set_secure_cookie(u'scientist', scientist_id)
        self.redirect(u'/')


class LogoutHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        print u'logout'
        scientist_id = self.get_secure_cookie(u'scientist')
        if not scientist_id:
            raise Exception(u'WTF???')
        self.clear_cookie(u'scientist')
        self.redirect(self.get_argument(u'next', u'/'))