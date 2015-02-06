# -*- coding: utf-8 -*-

from tornado import gen
import logging
import momoko
from common.connections import PSQLClient

__author__ = 'mayns'


@gen.coroutine
def create_scientists_relation():
    logging.info(u'creating scientists relation')
    conn = PSQLClient.get_client()
    yield momoko.Op(conn.execute,
                    """CREATE TABLE scientists (
                    id bigserial primary key,
                    email text,
                    first_name text,
                    last_name text,
                    middle_name text,
                    dob date,
                    gender text,
                    image_small bytea,
                    image_medium bytea,
                    image_large bytea,
                    location_country text,
                    location_city text,
                    middle_education  json,
                    high_education  json,
                    publications  json,
                    interests  text,
                    project_ids  bigint[],
                    about  text,
                    contacts  json,
                    desired_projects_ids  bigint[],
                    managing_projects_ids  bigint[],
                    dt_created timestamptz,
                    dt_last_visit timestamptz);""")

create_scientists_relation()