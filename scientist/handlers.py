# -*- coding: utf-8 -*-

import json
from tornado import gen, web
import cStringIO
import environment
from PIL import Image
from base.handlers import BaseRequestHandler
from scientist.scientist_bl import ScientistBL
from common.media_server import upload

__author__ = 'oks'


class ScientistsListHandler(BaseRequestHandler):

    @gen.coroutine
    def get(self):
        print u'scientists list get'
        scientists = yield ScientistBL.get_all_scientists()
        if scientists is None:
            scientists = json.dumps({u'scientists': []})
        self.finish(scientists)


class ScientistHandler(BaseRequestHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        # create folder with user id
        # create folder /avatars in it
        print u'scientist post'
        scientist_dict = json.loads(self.get_argument(u'data', u'{}'))
        scientist_anw = yield ScientistBL.add_scientist(scientist_dict)
        if not isinstance(scientist_anw, dict) and u'Error' in str(scientist_anw):
            response = dict(message=scientist_anw)
            print response
            response_data = yield self.get_response(response)
            self.finish(response_data)
            return

        response = dict(id=str(scientist_anw))
        if (not self.request.files) or (u'photo' not in self.request.files):
            print 'NOPE'
            response_data = yield self.get_response(response)
            self.set_secure_cookie(u'scientist', str(scientist_anw))
            self.finish(response_data)
            return

        scientist_photo = self.request.files['photo'][0]
        img = Image.open(cStringIO.StringIO(scientist_photo.body))
        w, h = img.size
        diff = w - h
        if diff > 0:
            img = img.crop((diff / 2, 0, diff / 2 + h, h))
        if diff < 0:
            img = img.crop((0, 0, w, w))
        for size in environment.AVATAR_SIZES:
            new_img = img.resize((size, size), Image.ANTIALIAS)
            filename = u'{size}.bmp'.format(size=size)
            new_img = new_img.convert()
            yield upload(new_img.tobitmap(), u'a', filename)

        # yield upload(scientist_photo.body, u'a', u'test.bmp')
        response_data = yield self.get_response(response)
        self.set_secure_cookie(u'scientist', str(scientist_anw))
        self.finish(response_data)

    @gen.coroutine
    def put(self):
        print u'scientist put'
        scientist_dict = json.loads(self.get_argument(u'data', u'{}'))

        yield ScientistBL.update_scientist(scientist_dict[u'scientist'])
        response_data = yield self.get_response(dict())
        self.finish(response_data)

    @web.authenticated
    @gen.coroutine
    def get(self, scientist_id):
        response = yield ScientistBL.get_scientist(int(scientist_id.replace(u'/', u'')))
        response_data = yield self.get_response(response)
        self.finish(response_data)

    @gen.coroutine
    def delete(self, scientist_id):
        print u'scientist delete'
        yield ScientistBL.delete_scientist(scientist_id)
        response_data = yield self.get_response(dict())
        self.finish(response_data)
