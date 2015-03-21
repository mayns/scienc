# -*- coding: utf-8 -*-

import cStringIO
import logging

import momoko
from tornado import gen
from PIL import Image

import environment
from db.utils import get_select_query, get_insert_query
from common.media_server import upload, delete, get_url
from common.utils import set_password, check_password
from common.decorators import psql_connection
from scientist.models import Scientist
from common.exceptions import UserExistException, RequiredFields, PSQLException


__author__ = 'oks'


class ScientistBL(object):

    @classmethod
    @gen.coroutine
    def create(cls, scientist_dict=None, scientist_photo=None):

        # check if user can create account
        yield cls.validate_credentials(scientist_dict)
        # create account
        yield cls.update_roles(scientist_dict)

        validated_data = Scientist.get_validated_data(scientist_dict)

        scientist = Scientist(**validated_data)
        scientist_id = yield scientist.save(update=False)

        image_url = yield cls.upload_avatar(scientist_id, scientist_photo)
        if image_url:
            scientist = yield Scientist.get_by_id(scientist_id)
            scientist.image_url = image_url
            yield scientist.save(fields=[u'image_url'])

        image_url = environment.GET_IMG(image_url, environment.IMG_S) if image_url else u''
        raise gen.Return(dict(scientist_id=scientist_id, image_url=image_url))

    @classmethod
    @gen.coroutine
    def update(cls, scientist_dict, scientist_photo):
        scientist_id = scientist_dict.pop(u'scientist_id')

        if not scientist_id:
            raise Exception(u'No scientist id on update')

        scientist = yield Scientist.get_by_id(scientist_id)

        if scientist_photo:
            new_image_url = yield cls.upload_avatar(scientist_id, scientist_photo)
            if not scientist.image_url:
                scientist_dict.update(dict(
                    image_url=new_image_url
                ))

        validated_data = Scientist.get_validated_data(scientist_dict)
        updated_fields = scientist.populate_fields(validated_data)
        print 'UPDATED FIELDS: ', updated_fields
        yield scientist.save(fields=updated_fields)
        image_url = environment.GET_IMG(scientist.image_url, environment.IMG_S) if scientist.image_url else u''
        raise gen.Return(dict(scientist_id=scientist_id, image_url=image_url))

    @classmethod
    @gen.coroutine
    def upload_avatar(cls, scientist_id, scientist_photo):

        if not scientist_photo or (not scientist_photo.get(u'raw_image')):
            raise gen.Return(u'')

        file_path = environment.AVATAR_PATH(scientist_id)
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
        yield delete(environment.MEDIA_USR_PATH(scientist_id), u'')

    @classmethod
    @gen.coroutine
    @psql_connection
    def validate_credentials(cls, conn, data):

        """
        Check if user can save email/pwd

        :param conn:
        :param data:
        :raise gen.Return:
        """
        email = data.get(u'email')
        pwd = data.get(u'pwd')

        both_fields = email and pwd
        if not both_fields:
            raise RequiredFields([u'Email', u'Password'])

        sql_query = get_select_query(environment.ROLES_TABLE, functions="count(*)", where=dict(column=u'email',
                                                                                               value=email))
        cursor = yield momoko.Op(conn.execute, sql_query)
        count = cursor.fetchone()
        if int(count[0]) > 0:
            raise UserExistException(email)

    @classmethod
    @gen.coroutine
    @psql_connection
    def check_login(cls, conn, email, pwd):

        sql_query = get_select_query(environment.ROLES_TABLE, columns=['id', 'pwd'],
                                     where=dict(column='email', value=email))

        cursor = yield momoko.Op(conn.execute, sql_query)
        data = cursor.fetchone()
        if not data:
            raise Exception(u'Incorrect pwd')
        _id, enc_pwd = data
        exists = check_password(pwd, enc_pwd)
        if exists:
            raise gen.Return(int(_id))
        raise Exception(u'Incorrect pwd')

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
        sqp_query = get_insert_query(environment.ROLES_TABLE, params)

        yield momoko.Op(conn.execute, sqp_query)

    @classmethod
    @gen.coroutine
    def delete(cls, scientist_id):
        try:
            print 'deleting from postgres'
            yield Scientist.delete(scientist_id, tbl=environment.ROLES_TABLE)
        except PSQLException, ex:
            raise ex

        try:
            # remove avatar
            yield cls.remove_avatar(scientist_id)
        except Exception, ex:
            logging.exception(ex)

    @classmethod
    @gen.coroutine
    def get_all(cls):
        data = yield Scientist.get_all_json(columns=Scientist.OVERVIEW_FIELDS)
        scientists = []
        for d in data:
            image_url = d.get(u'image_url', u'') and environment.GET_IMG(d.get(u'image_url', u''), environment.IMG_L)
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
    def get(cls, scientist_id):

        """

        :param scientist_id:
        :type scientist_id: int
        :rtype: dict
        """
        data = yield Scientist.get_json_by_id(scientist_id)
        image_url = data.get(u'image_url', u'') and environment.GET_IMG(data.get(u'image_url', u''), environment.IMG_L)
        data.update(image_url=image_url)
        logging.info(data)
        raise gen.Return(data)