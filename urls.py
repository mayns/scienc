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
    (r"/api/scientists", ScientistsListHandler),
    (r"/api/scientists/add/", ScientistsListHandler),
    (r"/api/scientists/(\w+)", ScientistsListHandler),
    (r"/api/scientist/(\w+)", ScientistProfileHandler),
    (r"/ajax/scientists/login/", AjaxScientistLoginHandler),

    # projects
    (r"/api/project/add", ProjectListHandler),
    (r"/api/projects", ProjectListHandler),
    # (r"/ckeditor/samples/", CkeditorSampleHandler),

]
