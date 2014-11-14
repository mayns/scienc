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
import settings

if __name__ == "__main__":
    _ioloop = ioloop.IOLoop.instance()

    logging.info(u"keep calm, i'm logging")

    from common.psql_relations import create_db
    create_db()

    from common.psql_relations import create_relations
    _ioloop.run_sync(partial(create_relations))

    # from postgres_fill import insert_data
    # _ioloop.run_sync(partial(insert_data, settings.PSQL_PARTITION_DEFAULT))

    # from postgres_fill import delete_kinder_garden
    # _ioloop.run_sync(partial(delete_kinder_garden, settings.PSQL_PARTITION_DEFAULT))

