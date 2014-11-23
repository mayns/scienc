# -*- coding: utf-8 -*-

from tornado import web, gen
import json
import urllib
import hashlib
from common.utils import generate_id, set_password, check_password
from scientist.scientist_bl import ScientistBL

__author__ = 'oks'


class AjaxScientistNewHandler(web.RequestHandler):
    @gen.coroutine
    def post(self):
        response = {'status': 'ok'}
        print self.parse_arguments()
        size = 40
        try:
            scientist = self.get_argument(u'scientist', u'{}')
            scientist = json.loads(scientist)
            scientist[u'id'] = scientist[u'id'] if scientist[u'id'] else generate_id(10)
            email = scientist[u'email']

            # construct the urls
            gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
            gravatar_url += urllib.urlencode({'s': str(size)})
            scientist[u'image'] = gravatar_url
            yield ScientistBL.save_to_redis(scientist)
        except Exception, ex:
            response = {'status': 'not ok'}
            print ex
        self.finish(response)


class AjaxScientistLoginHandler(web.RequestHandler):
    @gen.coroutine
    def post(self):
        response = {'status': 'not ok'}
        try:
            ajax_params = self.get_argument(u"scientist")
            log_pass = json.loads(ajax_params)
            login = log_pass.get(u'login_email')
            enc_password = yield ScientistBL.check_user_exist(login)
            password = log_pass.get(u'login_password')
            if not login or not password or not enc_password:
                response = {'status': 'not ok'}
            if check_password(password, enc_password):
                response = {'status': 'ok'}
            print password
            print enc_password
        except Exception, ex:
            response = {'status': 'not ok', 'message': ex}
            print ex
        self.finish(response)