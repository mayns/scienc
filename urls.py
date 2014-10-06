# -*- coding: utf-8 -*-

# from project.handlers import CkeditorSampleHandler
from common import handlers as cm_handlers
from project import handlers as pr_handlers
from scientist import handlers as sc_handlers
from scientist import ajax_handlers as sc_ajax_handlers

__author__ = 'oks'

url_handlers = [
    # common
    (r"/", cm_handlers.HomeHandler),
    (r"/not-found", cm_handlers.NotFoundHandler),

    # scientists
    (r"/scientists", sc_handlers.ScientistsListHandler),
    (r"/scientists/add/", sc_handlers.ScientistsListHandler),
    (r"/scientists/(\w+)", sc_handlers.ScientistsListHandler),
    (r"/scientist/(\w+)", sc_handlers.ScientistProfileHandler),
    (r"/ajax/scientists/login/", sc_ajax_handlers.AjaxScientistLoginHandler),

    # projects
    (r"/project/add", pr_handlers.ProjectListHandler),
    (r"/projects", pr_handlers.ProjectListHandler),
    # (r"/ckeditor/samples/", CkeditorSampleHandler),

]
