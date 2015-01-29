# -*- coding: utf-8 -*-

import settings
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

__author__ = 'mayns'

MEDIA_SERVER_UPLOAD_URL = u"http://{host}/uploads/{entity}/{filename}"


@gen.coroutine
def upload(body, entity, filename):
    params = dict(
        host=settings.MEDIA_SERVER_HOST,
        entity=entity,
        filename=filename
    )
    url = MEDIA_SERVER_UPLOAD_URL.format(**params)
    try:
        yield AsyncHTTPClient().fetch(url, method='PUT', body=body)
    except Exception, ex:
        print ex
    print url
    raise gen.Return(url)