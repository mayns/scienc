# -*- coding: utf-8 -*-

__author__ = 'mayns'


#---------- SCIENCE FIELDS ----------#

MATH = u'Математика, информатика и механика'
PHYSICS = u'Физика и астрономия'
CHEMISTRY = u'Химия'
BIOLOGY = u'Биология и медицинская наука'
EARTH = u'Науки о Земле'
ENGINEERING = u'Инженерные науки'
IT = u'Информационные технологии и вычислительные системы'

SCIENCE_FIELDS = [MATH, PHYSICS, CHEMISTRY, BIOLOGY, EARTH, ENGINEERING, IT]


#-------- ORGANIZATION TYPES --------#

PRIVATE = u'private'
GROUP = u'group'
UNIVERSITY = u'university'
INSTITUTION = u'institution'

ORGANIZATION_TYPES = [PRIVATE, GROUP, UNIVERSITY, INSTITUTION]


#---------- CONTACT TYPES -----------#

PHONE = u'phone'
SKYPE = u'skype'
EMAIL = u'email'

CONTACT_TYPES = [PHONE, SKYPE, EMAIL]


#------------ IMAGE SIZES ------------#

AVATAR_SIZES = [60, 100, 250]

IMAGE_URL_MENU = lambda img_url: u'{}60.png'.format(img_url)
IMAGE_URL_LIST = lambda img_url: u'{}100.png'.format(img_url)
IMAGE_URL_PROFILE = lambda img_url: u'{}250.png'.format(img_url)


DATETIME_FORMAT = dict(
    date=dict(
        DB=u'%Y-%d-%m',
        HUMAN=u'%d-%m-%Y'
    ),
    timestamp=dict(
        DB=u'%Y-%d-%m %H:%M:%S',
        HUMAN=u'%d-%m-%Y %H:%M:%S'
    )
)

ROLES_TABLE = u'roles'

ROLE_ADMIN = 1
ROLE_USER = 2