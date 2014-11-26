# -*- coding: utf-8 -*-

# from project.handlers import CkeditorSampleHandler
from common import handlers as cm_handlers
from project import handlers as pr_handlers
from scientist import handlers as sc_handlers
from scientist import ajax_handlers as sc_ajax_handlers

__author__ = 'oks'

url_handlers = [
    # common
    # (r"/", cm_handlers.HomeHandler),
    (r"/api/login", cm_handlers.LoginHandler),
    (r"/api/logout", cm_handlers.LogoutHandler),
    # (r"/not-found", cm_handlers.NotFoundHandler),

    # scientists
    (r"/api/scientist/(\w+)?", sc_handlers.ScientistHandler),
    (r"/api/scientists", sc_handlers.ScientistsListHandler),

    # projects
    (r"/api/project/(\w+)", pr_handlers.ProjectHandler),
    (r"/api/projects", pr_handlers.ProjectsListHandler),
    # (r"/ckeditor/samples/", CkeditorSampleHandler),

]
