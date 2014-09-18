# -*- coding: utf-8 -*-

from importlib import import_module
from inspect import getmembers, isfunction
global jinja_template_loader
from tornado.template import BaseLoader
from jinja2 import FileSystemLoader, Environment, ChoiceLoader, TemplateNotFound, Template
import settings

__author__ = 'oks'


class TemplateLoader(BaseLoader):
    def __init__(self, autoescape="xhtml_escape", namespace=None):
        super(TemplateLoader, self).__init__(autoescape, namespace)
        templates = getattr(settings, 'TEMPLATE_DIRS', [])
        global_exts = getattr(settings, 'JINJA_EXTS', ())
        self.jinja_env = Environment(extensions=global_exts, loader=ChoiceLoader([FileSystemLoader(templates)]))
        self.jinja_env.template_class = Template
        jinjaFilters = {}
        for jinja_filter in settings.JINJA_FILTERS:
            module = import_module(jinja_filter)
            for name, function in getmembers(module):
                if isfunction(function):
                    jinjaFilters[name] = function
        if jinjaFilters:
            self.jinja_env.filters = jinjaFilters

    def get_template(self, template_name):
        template = None
        try:
            template = self.jinja_env.get_template(template_name)
        except TemplateNotFound:
            pass
        return template

    def render_to_string(self, fileName, context=None):
        if context is None:
            context = {}

        template = self.get_template(fileName)
        return template.render(context)

jinja_template_loader = TemplateLoader()


def render_to_string(fileName, context=None):
    try:
        if context is None:
            context = {}

        template = jinja_template_loader.get_template(fileName)
        return template.render(context)
    except Exception, ex:
        print "Error: render_to_string: file_name = %s: ex=%s" % (fileName, ex)
        return ""