# -*- coding: utf-8 -*-

from tornado import ioloop
import time
__author__ = 'nyash myash'

if __name__ == "__main__":
    from redis_fill import *

    _ioloop = ioloop.IOLoop.instance()

    start = time.time()
    _ioloop.run_sync(add_data)
    finish = time.time()
    print finish-start

    start = time.time()
    _ioloop.run_sync(add_filters)
    finish = time.time()
    print finish-start

