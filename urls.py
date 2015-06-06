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
    (r"/api/user(/)?", cm_handlers.UserHandler),

    # scientists
    (r"/api/scientists(/\w+)?", sc_handlers.ScientistHandler),
    (r"/api/scientists/search", sc_handlers.ScientistsSearchHandler),
    (r"/api/scientists/role", sc_handlers.ScientistRoleHandler),
    (r"/api/scientists/my-projects", sc_handlers.ScientistManagedProjectsHandler),
    (r"/api/scientists/participation", sc_handlers.ScientistParticipationProjectsHandler),
    (r"/api/scientists/desired", sc_handlers.ScientistDesiredProjectsHandler),

    # projects
    (r"/api/projects(/\w+)?", pr_handlers.ProjectHandler),
    (r"/api/projects/search", pr_handlers.ProjectsSearchHandler),
    (r"/api/projects/(\w+)/like", pr_handlers.ProjectsLikeHandler),
    (r"/api/projects/(\w+)/responses/?", pr_handlers.ResponseHandler),
    # (r"/api/projects/(\w+)/participation", pr_handlers.ProjectsParticipationHandler),
    # (r"/ckeditor/samples/", CkeditorSampleHandler),

    # test stands
    (r"/api/stand/items", st_handlers.ServerGenTemplateItemsHandler),
    (r"/api/stand/item(/\d+)?", st_handlers.ServerGenTemplateItemHandler),


    (r"/api/.*", cm_handlers.NotFoundRedirectHandler),

]