# -*- coding: utf-8 -*-

from tornado import gen
from base.handlers import BaseRequestHandler
from project.project_bl import ProjectBL

__author__ = 'mayns'


class ServerGenTemplateHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        projects = yield ProjectBL.get_all()
        self.render("projects_list.html", projects=projects)
