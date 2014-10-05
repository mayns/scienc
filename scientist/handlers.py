# -*- coding: utf-8 -*-

import json
import urllib
import hashlib
from tornado import gen
from base.handlers import BaseRequestHandler
from scientist.scientist_bl import ScientistBL

__author__ = 'oks'


class ScientistNewHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):

        email = 'oksgorobets@gmail.com'
        size = 40
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'s': str(size)})
        image_url = gravatar_url
        # print image_url
        self.render(u'/scientists/register_user.html', {u'image_url': image_url})


class ScientistsListHandler(BaseRequestHandler):
    def gravatar(self):
        email = 'oksgorobets@gmail.com'
        size = 40
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'s': str(size)})
        return gravatar_url

    @gen.coroutine
    def get(self):
        scientists = yield ScientistBL.get_all_scientists()
        if scientists is None:
            scientists = json.dumps({'scientists': []})
        # print scientists
        self.finish(scientists)

    @gen.coroutine
    def post(self, *args, **kwargs):
        scientist_dict = json.loads(self.request.body)
        if ScientistBL.validate_data(scientist_dict):
            scientist_id = yield ScientistBL.add_scientist(scientist_dict[u'scientist'])
        else:
            raise Exception(u'Not valid data')
        scientist_dict['scientist'].update(dict(id=scientist_id))
        self.finish(json.dumps(scientist_dict))

    @gen.coroutine
    def delete(self, scientist_id):
        yield ScientistBL.delete_scientist(scientist_id)
        self.finish()


class ScientistProfileHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.render(u'/scientists/user_profile.html')


class ScientistProfileEditHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.render(u'/scientists/profile_management.html')
