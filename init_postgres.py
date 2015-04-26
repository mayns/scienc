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

    logging.info(u"keep calm, i'm logging")

    from db.psql_relations import create_db
    create_db()

    from db.psql_relations import create_config
    _ioloop.run_sync(partial(create_config))

    from db.psql_relations import create_relations
    _ioloop.run_sync(partial(create_relations))


    # from postgres_fill import insert_data
    # _ioloop.run_sync(partial(insert_data))

    # from postgres_fill import delete_kinder_garden
    # _ioloop.run_sync(partial(delete_kinder_garden))

    # from postgres_fill import add_test_project
    # _ioloop.run_sync(add_test_project)
