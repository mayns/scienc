# -*- coding: utf-8 -*-

__author__ = 'mayns'


# ---------- SCIENCE FIELDS ---------- #

V_MATH = u'Математика, информатика и механика'
V_PHYSICS = u'Физика и астрономия'
V_CHEMISTRY = u'Химия'
V_BIOLOGY = u'Биология и медицинская наука'
V_EARTH = u'Науки о Земле'
V_ENGINEERING = u'Инженерные науки'
V_IT = u'Информационные технологии и вычислительные системы'

K_MATH = u'math'
K_PHYSICS = u'physics'
K_CHEMISTRY = u'chemistry'
K_BIOLOGY = u'biology'
K_EARTH = u'earth'
K_ENGINEERING = u'engineering'
K_IT = u'it'

SCIENCE_FIELDS_MAP = {
    K_MATH: V_MATH,
    K_PHYSICS: V_PHYSICS,
    K_CHEMISTRY: V_CHEMISTRY,
    K_BIOLOGY: V_BIOLOGY,
    K_EARTH: V_EARTH,
    K_ENGINEERING: V_ENGINEERING,
    K_IT: V_IT,
}


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
        DB=u'%Y-%m-%d',
        HUMAN=u'%d.%m.%Y'
    ),
    timestamp=dict(
        DB=u'%Y-%m-%d %H:%M:%S',
        HUMAN=u'%d.%m.%Y %H:%M:%S'
    )
)

TABLE_ROLES = u'roles'
TABLE_VACANCIES = u'vacancies'
TABLE_PARTICIPANTS = u'participants'
TABLE_RESPONSES = u'responses'

ROLE_ADMIN = 1
ROLE_USER = 2

STATUS_ACCEPTED = u'accepted'
STATUS_DECLINED = u'declined'
STATUS_WAITING = u'waiting'
STATUS_DELETED = u'deleted'