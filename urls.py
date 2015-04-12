# -*- coding: utf-8 -*-

# from project.handlers import CkeditorSampleHandler
from common import handlers as cm_handlers
from project import handlers as pr_handlers
from scientist import handlers as sc_handlers
from stands import handlers as st_handlers

__author__ = 'oks'
url_handlers = [
    # common
    (r"/api/login", cm_handlers.LoginHandler),
    (r"/api/logout", cm_handlers.LogoutHandler),
    (r"/api/not-found", cm_handlers.NotFoundHandler),
    (r"/api/xsrf", cm_handlers.CSRFHandler),
    (r"/api/user", cm_handlers.UserHandler),

    # scientists
    (r"/api/scientist(/\d+)?", sc_handlers.ScientistHandler),
    (r"/api/scientist/role", sc_handlers.ScientistRoleHandler),
    (r"/api/scientists", sc_handlers.ScientistsListHandler),
    (r"/api/scientist/my-projects", sc_handlers.ScientistManagedProjectsHandler),
    (r"/api/scientist/participation", sc_handlers.ScientistParticipationProjectsHandler),
    (r"/api/scientist/desired", sc_handlers.ScientistDesiredProjectsHandler),

    # projects
    (r"/api/project(/\d+)?", pr_handlers.ProjectHandler),
    (r"/api/projects", pr_handlers.ProjectsListHandler),
    (r"/api/project/(\d+)/like", pr_handlers.ProjectsLikeHandler),
    (r"/api/project/(\d+)/responses/[a|d]?", pr_handlers.ProjectsResponseHandler),
    (r"/api/project/(\d+)/participation", pr_handlers.ProjectsParticipationHandler),
    # (r"/ckeditor/samples/", CkeditorSampleHandler),

    # test stands
    (r"/stand/i/gen-templates/items", st_handlers.ServerGenTemplateItemsHandler),
    (r"/stand/i/gen-templates/item(/\d+)?", st_handlers.ServerGenTemplateItemHandler),


    (r"/api/.*", cm_handlers.NotFoundRedirectHandler),

]

