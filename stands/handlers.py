# -*- coding: utf-8 -*-

from base.handlers import BaseRequestHandler

__author__ = 'mayns'


class ServerGenTemplateHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        self.write(self.template_loader.load("projects_list.html").generate(name="Alice", where=u'in Wonderland'))