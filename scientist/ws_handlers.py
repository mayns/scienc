# -*- coding: utf-8 -*-
from tornado import gen, websocket

__author__ = 'oks'


class ScientistRegisterWSHandler(websocket.WebSocketHandler):

    @gen.coroutine
    def on_message(self, message):
        print 'in socket handler'
        print message