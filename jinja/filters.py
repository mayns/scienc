# -*- coding: utf-8 -*-


__author__ = 'oks'


def static_url(path, *args):
    """
    @param value: str
    @return: str
    """
    res_url = u'{x_scheme}://{host}/static/{value}'.format(
        x_scheme=u'http',
        host=u'sciencemates.dev',
        value=path
    )
    return res_url