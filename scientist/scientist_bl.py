# -*- coding: utf-8 -*-

import cStringIO

import momoko
from tornado import gen
from PIL import Image

import settings
import environment
from db.utils import get_insert_sql_query
from common.media_server import upload, get_url
from common.utils import set_password, check_password
from common.decorators import psql_connection
from scientist.models import Scientist
from common.exceptions import UserExistException, RequiredFields


__author__ = 'oks'


class ScientistBL(object):

    @classmethod
    @gen.coroutine
    def create(cls, scientist_dict=None, scientist_photo=None):

        # check if user can save email/pwd and save it if he can
        yield cls.validate_data(scientist_dict)
        yield cls.update_roles(scientist_dict)

        scientist = Scientist(**scientist_dict)
        scientist_id = yield scientist.save(update=False)

        image_url = yield cls.upload_avatar(scientist_id, scientist_photo)
        if image_url:
            scientist = yield Scientist.get_by_id(scientist_id)
            scientist.image_url = image_url
            yield scientist.save(fields=[u'image_url'])

        raise gen.Return(dict(scientist_id=scientist_id, image_url=environment.IMAGE_URL_MENU(image_url)))


    @classmethod
    @gen.coroutine
    def update(cls, scientist_id, scientist_dict, scientist_photo):
        scientist = yield Scientist.get_by_id(scientist_id)
        image_url = scientist.image_url + u'50.png'
        if scientist_photo:
            image_url = yield cls.upload_avatar(scientist_id, scientist_photo[0])
            scientist_dict.update(dict(
                image_url=image_url
            ))
        scientist.populate_fields(scientist_dict)
        yield scientist.save()

    @classmethod
    @gen.coroutine
    def upload_avatar(cls, scientist_id, scientist_photo):

        if not scientist_photo.get(u'raw_image'):
            raise gen.Return(u'')

        file_path = u'{sc_id}/a'.format(sc_id=str(scientist_id))
        url_path = get_url(file_path)

        img = Image.open(cStringIO.StringIO(scientist_photo[u'raw_image'][0].body))
        c = scientist_photo.get(u'raw_image_coords', {})

        # crop by coordinates from client or default from the top 250x250 --- ? make square as before
        img = img.crop((int(c.get(u'x1', 0)), int(c.get(u'y1', 0)), int(c.get(u'x2', 250)),
                        int(c.get(u'y2', 250))))

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

        both_fields = email and pwd
        if not both_fields:
            raise RequiredFields([u'Email', u'Password'])

        cursor = yield momoko.Op(conn.execute, u"SELECT count(*) FROM {table_name} WHERE email='{email}'".format(
            table_name=environment.ROLES_TABLE,
            email=email))
        count = cursor.fetchone()
        if int(count[0]) > 0:
            raise UserExistException(email)

    @classmethod
    @gen.coroutine
    @psql_connection
    def check_scientist(cls, conn, email, pwd):

        cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE email='{email}'".format(
            columns='pwd',
            table_name=environment.ROLES_TABLE,
            email=email))
        enc_pwd = cursor.fetchone()
        if not enc_pwd:
            raise Exception(u'Incorrect pwd')
        exists = check_password(pwd, enc_pwd[0])
        if exists:
            cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE email='{email}'".format(
                columns=u'id',
                table_name=Scientist.TABLE,
                email=email))
        _id = cursor.fetchone()[0]
        raise gen.Return(int(_id))

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
            image_url = d.get(u'image_url', u'') and d.get(u'image_url', u'') + u'100.png'
            scientists.append(dict(
                id=d[u'id'],
                image_url=image_url,
                full_name='{} {} {}'.format(d.get(u'first_name', u''), d.get(u'middle_name', u''), d.get(u'last_name', u'')),
                location='{} {}'.format(d.get(u'city', u''), d.get(u'country', u'')),
                projects=len(d.get(u'participating_projects', []))
            ))
        raise gen.Return(scientists)

    @classmethod
    @gen.coroutine
    def get_scientist(cls, scientist_id):
        data = yield Scientist.get_json_by_id(scientist_id)
        raise gen.Return(data)