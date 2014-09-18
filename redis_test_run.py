# -*- coding: utf-8 -*-

from tornado import ioloop
import time

__author__ = 'nyash myash'

if __name__ == "__main__":
    from redis_test import *

    _ioloop = ioloop.IOLoop.instance()

    start = time.time()
    _ioloop.run_sync(test)
    finish = time.time()
    print finish-start

