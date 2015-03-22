# -*- coding: utf-8 -*-

import os
import logging
import sys
from functools import partial


__author__ = 'mayns'

path = os.path.abspath(__file__)
sys.path.append(os.path.join(os.path.dirname(path), "../"))
os.environ['PROJECT_SETTINGS_MODULE'] = 'settings'

from tornado import ioloop

if __name__ == "__main__":
    _ioloop = ioloop.IOLoop.instance()

    from db.psql_relations import create_relations
    _ioloop.run_sync(partial(create_relations))

    from db.postgres_fill import fill_init_data
    _ioloop.run_sync(fill_init_data)
