# -*- coding: utf-8 -*-

from common.descriptors import *

__author__ = 'mayns'


MODELS = dict(
    scientists={

        # common info
        u'id': ID(),
        u'pwd': Text(),
        u'email': Text(),
        u'first_name': Text(),
        u'last_name': Text(),
        u'middle_name': Text(),
        u'dob': Datetime(),
        u'gender': Text(),
        u'image_url': Text(),
        u'location': JsonObject(),

        # professional info
        u'middle_education': JsonArray(),    # [{country, city, university, faculty, chair, graduation_year, graduation_level}]
        u'high_education': JsonArray(),
        u'publications': JsonArray(),
        u'interests': JsonArray(),
        u'about': JsonArray(),
        u'contacts': JsonArray(),

        # app activity
        u'participate_in_projects': JsonArray(),       # [{project_id, role_id}]
        u'desired_vacancies': JsonArray(),             # [{project_id, vacancy_id}]
        u'managing_projects_ids': JsonArray(),
        u'achievements': JsonArray(),                  # [achievement_id]

        # system info
        u'dt_created': Datetime(),
    },

    # projects={
    #     u'scientist_id': TYPE_INT,     # person added the project
    #     u'lang': TYPE_STRING,
    #     u'research_fields': TYPE_LIST,  # области науки
    #     u'title': TYPE_STRING, # название проекта
    #     u'description_short': TYPE_STRING,  # краткое описание для обложки
    #     u'views': TYPE_INT,  # количество просмотров
    #     u'likes': TYPE_INT,  # количество лайков
    #     u'responses': TYPE_LIST,  # ids отклкнувшихся юзеров
    #     u'organization_type': TYPE_STRING,  # личный, групповой, под эгидой организации, университет
    #     u'organization_location': TYPE_JSON,  # страна, город
    #     u'organization_structure': TYPE_JSON,  # ~ university, faculty, chair -- только у организации и универа - hstore
    #
    #     u'start_date': TYPE_DATE,  # начало работы
    #     u'end_date': TYPE_DATE,  # планиуремая дата окончания если есть
    #     u'objective': TYPE_STRING,  # цель исследования
    #     u'description_full': TYPE_STRING,  # полное описание
    #     u'usage_possibilities': TYPE_STRING,  # возможности применения результатов
    #     u'results': TYPE_STRING,  # достигнутые результаты и практическое применение
    #     u'related_data': TYPE_LIST,  # дополнительные данные -- [{'id', 'source', 'description'}]
    #     u'leader': TYPE_STRING,  # руководитель проекта
    #     u'participants': TYPE_LIST,  # участники с ролями -- [{'id', 'role', 'name': str, <'user_id', 'verified': bool>}]
    #     u'missed_participants': TYPE_LIST,  # кого не хватает -- [{'id': int, 'role': str, 'description': str}]
    #     u'tags': TYPE_LIST,  # тэги
    #
    #     u'contact_manager': TYPE_STRING,  # ответственный за связь
    #     u'contacts': TYPE_LIST,  # способы связи -- [{'type', 'number'}]
    #     u'project_site': TYPE_STRING,
    #
    #     u'dt_created': TYPE_DATE,
    #     u'dt_updated': TYPE_DATE,
    # }
)