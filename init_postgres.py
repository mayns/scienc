# -*- coding: utf-8 -*-


import os
import logging
import sys
from postgres_fill import insert_data, delete_kinder_garden
from functools import partial


__author__ = 'mayns'

path = os.path.abspath(__file__)
sys.path.append(os.path.join(os.path.dirname(path), "../"))
os.environ['PROJECT_SETTINGS_MODULE'] = 'settings'
# os.environ['PROJECT_ENVIRONMENT_MODULE'] = 'environment'

from tornado import ioloop
import settings

if __name__ == "__main__":
    _ioloop = ioloop.IOLoop.instance()

    logging.info(u'test_logging')

    from common.psql_relations import create_relations #, create_dbs
    #create_dbs()


    _ioloop.run_sync(partial(create_relations, settings.PSQL_PARTITION_DEFAULT))

    # _ioloop.run_sync(partial(insert_data, settings.PSQL_PARTITION_DEFAULT))
    # _ioloop.run_sync(partial(delete_kinder_garden, settings.PSQL_PARTITION_DEFAULT))

