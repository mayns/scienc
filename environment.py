# -*- coding: utf-8 -*-

__author__ = 'mayns'


# ---------- SCIENCE FIELDS ---------- #

MATH = u'Математика, информатика и механика'
PHYSICS = u'Физика и астрономия'
CHEMISTRY = u'Химия'
BIOLOGY = u'Биология и медицинская наука'
EARTH = u'Науки о Земле'
ENGINEERING = u'Инженерные науки'
IT = u'Информационные технологии и вычислительные системы'

SCIENCE_FIELDS = [MATH, PHYSICS, CHEMISTRY, BIOLOGY, EARTH, ENGINEERING, IT]

SCIENCE_FIELDS_MAP = dict(
    math=MATH,
    physics=PHYSICS,
    chemistry=CHEMISTRY,
    biology=BIOLOGY,
    earth=EARTH,
    engineering=ENGINEERING,
    it=IT,
)


# ---------- CONTACT TYPES ----------- #

PHONE = u'phone'
SKYPE = u'skype'
EMAIL = u'email'

CONTACT_TYPES = [PHONE, SKYPE, EMAIL]


# ------------ IMAGE SIZES ------------ #

AVATAR_SIZES = [60, 100, 250]

IMG_S = 60
IMG_M = 100
IMG_L = 250

GET_IMG = lambda url, size: u'{url}{size}.png'.format(url=url, size=size) if not u'gravatar' in url \
    else u'{url}?size={size}'.format(url=url, size=size)

IMAGE_URL_MENU = lambda img_url: u'{}60.png'.format(img_url)
IMAGE_URL_LIST = lambda img_url: u'{}100.png'.format(img_url)
IMAGE_URL_PROFILE = lambda img_url: u'{}250.png'.format(img_url)

AVATAR_PATH = lambda sc_id: u'{sc_id}/a'.format(sc_id=str(sc_id))
MEDIA_USR_PATH = lambda sc_id: str(sc_id)

DATETIME_FORMAT = dict(
    date=dict(
        DB=u'%Y-%d-%m',
        HUMAN=u'%d.%m.%Y'
    ),
    timestamp=dict(
        DB=u'%Y-%d-%m %H:%M:%S',
        HUMAN=u'%d.%m.%Y %H:%M:%S'
    )
)

ROLES_TABLE = u'roles'

ROLE_ADMIN = 1
ROLE_USER = 2