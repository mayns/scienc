# -*- coding: utf-8 -*-

import timeit
from functools import partial

__author__ = 'mayns'


from tornado import ioloop

if __name__ == "__main__":
    _ioloop = ioloop.IOLoop.instance()

    print 'Started generating data into /gen/scienc/post_data.txt'
    start = timeit.default_timer()

    from benchmarks.generators import generate_projects_to_file
    _ioloop.run_sync(partial(generate_projects_to_file))

    # from benchmarks.generators import generate_post_req_siege
    # _ioloop.run_sync(partial(generate_post_req_siege))

    print 'Generation finished in: {0:.2f} sec'.format(timeit.default_timer() - start)
