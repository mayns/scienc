# -*- coding: utf-8 -*-

from tornado import web
import logging
import sys

__author__ = 'oks'


class BaseRequestHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.payload = dict()
        super(BaseRequestHandler, self).__init__(*args, **kwargs)

    def get_current_user(self):
        return self.get_secure_cookie(u"scientist")

    def render(self, template, context=None):
        if context is None:
            context = {}
        response_html = self.render_string(template, context)
        self.finish(response_html)

    def render_error(self, ex, context=None):
        if context is None:
            context = {}
        logging.exception(ex)

        context.update(dict(
            exception=ex.message if ex.message else ex
        ))
        self.render('error_page.html', context)

    def render_string(self, template_file_name, context=None):
        try:
            if context is None:
                context = {}
            self.payload.update(context)
            template = self.application.template_loader.get_template(template_file_name)
            if not template:
                raise Exception("Template {0} not found".format(template_file_name))
            response_html = template.render(self.payload)
        except Exception, ex:
            logging.exception(ex)
            template = self.application.template_loader.get_template('error_page.html')
            ex_type, ex_val, ex_trace = sys.exc_info()
            self.payload.update(dict(
                exception=ex,
                ex_type=ex_type,
                ex_val=ex_val,
                ex_trace=ex_trace,
                request=self.request
            ))
            response_html = template.render(self.payload)
        return response_html


class LoginHandler(BaseRequestHandler):
    def post(self):
        self.set_secure_cookie(u'scientist', self.get_argument(u'name'))
        self.finish()