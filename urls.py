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
    (r"/scientists/(\w+)", sc_handlers.ScientistHandler),
    (r"/ajax/scientists/login/", sc_ajax_handlers.AjaxScientistLoginHandler),

    # projects
    (r"/projects/(\w+)", pr_handlers.ProjectHandler),
    # (r"/ckeditor/samples/", CkeditorSampleHandler),

]
