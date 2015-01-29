# -*- coding: utf-8 -*-

import settings
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

__author__ = 'mayns'

MEDIA_SERVER_UPLOAD_URL = u"http://{host}/uploads/{filepath}/{filename}"


@gen.coroutine
def upload(body, filepath, filename):
    params = dict(
        host=settings.MEDIA_SERVER_HOST,
        filepath=filepath,
        filename=filename
    )
    url = MEDIA_SERVER_UPLOAD_URL.format(**params)
    try:
        yield AsyncHTTPClient().fetch(url, method='PUT', body=body)
    except Exception, ex:
        print ex
    print url
    raise gen.Return(url)