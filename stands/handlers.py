# -*- coding: utf-8 -*-

from base.handlers import BaseRequestHandler

__author__ = 'mayns'


class ServerGenTemplateHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        self.render("projects_list.html", name="Alice", where=u'in Wonderland')
