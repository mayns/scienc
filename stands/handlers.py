# -*- coding: utf-8 -*-

import logging
from tornado import gen
from base.handlers import BaseRequestHandler
from project.project_bl import ProjectBL

__author__ = 'mayns'


class ServerGenTemplateItemsHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        projects = yield ProjectBL.get_all()
        self.render("projects_list.html", projects=projects)


class ServerGenTemplateItemHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self, project_id):
        project = {}
        try:
            project_id = int(project_id.replace(u'/', u''))
        except:
            self.send_error(status_code=403)
        print u'get server side project:', project_id

        try:
            project = yield ProjectBL.get(project_id)
        except Exception, ex:
            logging.info('Exc on get project: {}'.format(project_id))
            logging.exception(ex)

        self.render("project.html", project=project)
