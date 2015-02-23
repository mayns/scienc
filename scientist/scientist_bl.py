# -*- coding: utf-8 -*-

import cStringIO

import momoko
from tornado import gen
from PIL import Image

import settings
import environment
from db.tables import TABLES
from db.utils import get_insert_sql_query
from common.media_server import upload, get_url
from common.utils import set_password, check_password
from common.decorators import psql_connection
from scientist.models import Scientist
from common.exceptions import UserExistException


__author__ = 'oks'


class ScientistBL(object):

    @classmethod
    @gen.coroutine
    def modify(cls, scientist_dict=None, scientist_photo=None):

        # TODO: check updated fields
        # TODO: delete avatar marker
        scientist_id = scientist_dict.get(u'id', 0)

        try:
            if not scientist_id:
                scientist = Scientist(**scientist_dict)
                yield cls.validate_data(scientist_dict)
                print 'updating roles'
                yield cls.update_roles(scientist_dict)
                print scientist_dict
                scientist_id = yield scientist.save(update=False)
                if scientist_photo:
                    image_url = yield cls.upload_avatar(scientist_id, scientist_photo[0])
                    scientist = yield Scientist.get_by_id(scientist_id)
                    scientist.image_url = image_url
                    yield scientist.save(fields=[u'image_url'])
            else:
                scientist = yield Scientist.get_by_id(scientist_id)
                if scientist_photo:
                    image_url = yield cls.upload_avatar(scientist_id, scientist_photo[0])
                    scientist_dict.update(dict(
                        image_url=image_url
                    ))
                scientist.populate_fields(scientist_dict)
                yield scientist.save()
        except Exception, ex:
            print u'EXCEPTION IN MODIFY SCIENTIST: {}'.format(scientist_id), ex
            raise ex

        raise gen.Return(scientist_id)

    @classmethod
    @gen.coroutine
    def upload_avatar(cls, scientist_id, scientist_photo):

        file_path = u'{sc_id}/a'.format(sc_id=str(scientist_id))
        url_path = get_url(file_path)

        img = Image.open(cStringIO.StringIO(scientist_photo.body))
        w, h = img.size
        diff = w - h
        if diff > 0:
            img = img.crop((diff / 2, 0, diff / 2 + h, h))
        if diff < 0:
            img = img.crop((0, 0, w, w))
        for size in environment.AVATAR_SIZES:
            new_img = img.resize((size, size), Image.ANTIALIAS)
            filename = u'{size}.png'.format(size=size)
            out_im = cStringIO.StringIO()
            new_img.save(out_im, 'PNG')
            yield upload(out_im.getvalue(), file_path, filename)
        raise gen.Return(url_path)

    @classmethod
    @gen.coroutine
    def remove_avatar(cls, scientist_id):
        pass

    @classmethod
    @gen.coroutine
    @psql_connection
    def validate_data(cls, conn, data):
        email = data.get(u'email')
        pwd = data.get(u'pwd')
        if not all([email, pwd]):
            raise Exception(u'Email or password is missing')

        cursor = yield momoko.Op(conn.execute, u"SELECT count(*) FROM {table_name} WHERE email='{email}'".format(
            table_name=environment.ROLES_TABLE,
            email=email))
        count = cursor.fetchone()
        if int(count[0]) > 0:
            raise UserExistException(email)

    @classmethod
    @gen.coroutine
    @psql_connection
    def check_scientist(cls, conn, email, passw):

        cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE id='{id}'".format(
            columns=u', '.join(Scientist.CHARMED_COLUMNS),
            table_name=Scientist.CHARMED,
            id=email))
        enc_passw = cursor.fetchone()
        if not enc_passw:
            raise gen.Return()
        exists = check_password(passw, enc_passw[1])
        if exists:
            cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE email='{email}'".format(
                columns=u'id',
                table_name=Scientist.TABLE,
                email=email))
        id = cursor.fetchone()[0]
        raise gen.Return(unicode(id))

    @classmethod
    @gen.coroutine
    @psql_connection
    def update_roles(cls, conn, scientist_dict):
        pwd = set_password(scientist_dict.pop(u'pwd'))

        params = dict(
            email=scientist_dict.get(u'email'),
            pwd=pwd,
            role=scientist_dict.pop(u'role', environment.ROLE_USER)
        )
        sqp_query = get_insert_sql_query(environment.ROLES_TABLE, params)
        print sqp_query
        yield momoko.Op(conn.execute, sqp_query)

    @classmethod
    @gen.coroutine
    @psql_connection
    def remove_role(cls, conn, scientist_email):
        sqp_query = u"DELETE FROM {table_name} WHERE id='{id}'".format(table_name=environment.ROLES_TABLE,
                                                                       id=scientist_email)
        yield momoko.Op(conn.execute, sqp_query)

    @classmethod
    @gen.coroutine
    @psql_connection
    def delete_scientist(cls, conn, scientist_id):
        conn = conn.get_client(partition=settings.SCIENCE_DB)
        try:
            sqp_query = u"DELETE FROM {table_name} WHERE id = '{id}'".format(table_name=u'scientists', id=scientist_id)
            yield momoko.Op(conn.execute, sqp_query)
        except Exception, ex:
            print u'Exception in delete scientist', ex

    @classmethod
    @gen.coroutine
    def get_all_scientists(cls):
        data = yield Scientist.get_all_json(columns=Scientist.OVERVIEW_FIELDS)
        scientists = []
        for d in data:
            scientists.append(dict(
                full_name='{} {} {}'.format(d.get(u'first_name', u''), d.get(u'middle_name', u''), d.get(u'last_name', u'')),
                location='{} {}'.format(d.get(u'city', u''), d.get(u'country', u'')),
                projects=len(d.get(u'participating_projects', []))
            ))
        raise gen.Return(scientists)