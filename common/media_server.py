# -*- coding: utf-8 -*-

import settings
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

__author__ = 'mayns'

MEDIA_SERVER_UPLOAD_URL = u"http://{host}/uploads/{filepath}/{filename}"

MEDIA_SERVER_GET_URL = lambda file_path, file_name=u'', host=settings.MEDIA_SERVER_HOST: \
    u"http://{host}/uploads/{file_path}/{filename}".format(host=host, file_path=file_path, file_name=file_name)


@gen.coroutine
def upload(body, file_path, filename):
    params = dict(
        host=settings.MEDIA_SERVER_HOST,
        filepath=file_path,
        filename=filename
    )
    url = MEDIA_SERVER_UPLOAD_URL.format(**params)
    try:
        yield AsyncHTTPClient().fetch(url, method='PUT', body=body)
    except Exception, ex:
        print ex

    raise gen.Return(url)


def get_url(file_path, file_name=u''):
    return MEDIA_SERVER_GET_URL(file_path, file_name=file_name)