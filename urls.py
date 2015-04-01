# -*- coding: utf-8 -*-

# from project.handlers import CkeditorSampleHandler
from common import handlers as cm_handlers
from project import handlers as pr_handlers
from scientist import handlers as sc_handlers

__author__ = 'oks'
url_handlers = [
    # common
    (r"/api/login", cm_handlers.LoginHandler),
    (r"/api/logout", cm_handlers.LogoutHandler),
    (r"/api/not-found", cm_handlers.NotFoundHandler),
    (r"/api/xsrf", cm_handlers.CSRFHandler),
    (r"/api/user", cm_handlers.UserHandler),

    # scientists
    (r"/api/scientist", sc_handlers.ScientistHandler),
    (r"/api/scientist/role", sc_handlers.ScientistRoleHandler),
    (r"/api/scientists", sc_handlers.ScientistsListHandler),
    (r"/api/scientist/my-projects", sc_handlers.MyProjectsHandler),
    (r"/api/scientist/participating", sc_handlers.FavoriteParticipationProjectsHandler),
    (r"/api/scientist/applications", sc_handlers.FavoriteDesiredProjectsHandler),

    # projects
    (r"/api/project(/\d+)?", pr_handlers.ProjectHandler),
    (r"/api/projects", pr_handlers.ProjectsListHandler),
    (r"/api/project/(\d+)/like", pr_handlers.ProjectsLikeHandler),
    (r"/api/project/(\d+)/participation", pr_handlers.ProjectsParticipationHandler),
    # (r"/ckeditor/samples/", CkeditorSampleHandler),

    (r"/api/.*", cm_handlers.NotFoundRedirectHandler),

]

