# -*- coding: utf-8 -*-

from common.handlers import HomeHandler
# from project.handlers import CkeditorSampleHandler
from scientist.handlers import ScientistsListHandler, ScientistProfileHandler
from project.handlers import ProjectListHandler
from scientist.ajax_handlers import AjaxScientistLoginHandler

__author__ = 'oks'

url_handlers = [
    (r"/", HomeHandler),

    # scientists
    (r"/scientists", ScientistsListHandler),
    (r"/scientists/add/", ScientistsListHandler),
    (r"/scientists/(\w+)", ScientistsListHandler),
    (r"/scientist/(\w+)", ScientistProfileHandler),
    (r"/ajax/scientists/login/", AjaxScientistLoginHandler),

    # projects
    (r"/project/add", ProjectListHandler),
    (r"/projects", ProjectListHandler),
    # (r"/ckeditor/samples/", CkeditorSampleHandler),

]
