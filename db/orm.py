# -*- coding: utf-8 -*-

from common.descriptors import *

__author__ = 'mayns'


MODELS = dict(
    scientists = {

        # common info
        u'id': ID(db_references='roles(id)'),
        u'email': Text(required=True),
        u'first_name': Text(required=True),
        u'last_name': Text(required=True),
        u'middle_name': Text(),
        u'dob': Datetime(db_type='date'),
        u'gender': Text(),
        u'image_url': Text(),
        u'location': JsonObject(),                                                  # {country, city}

        # professional info
        u'middle_education': JsonObject(),                                          # {country, city, school, graduation_year}
        u'high_education': JsonArray(db_type='json'),                               # [{country, city, university, faculty, chair, degree, graduation_year}]
        u'publications': JsonArray(db_type='json'),                                 # [{id, title, source, year, link}]
        u'interests': JsonArray(db_type='text[]'),
        u'about': Text(),
        u'contacts': JsonArray(db_type='json'),                                     # [{type, id}]

        # app activity
        u'participating_projects': JsonArray(db_type='json'),                       # [{project_id, role_id}]
        u'desired_vacancies': JsonArray(db_type='json'),                            # [{project_id, vacancy_id}]
        u'managing_project_ids': JsonArray(db_type='bigint[]'),
        u'achievements': JsonArray(db_type='bigint[]'),                             # [achievement_id]

        # system info
        u'dt_created': Datetime(db_type='timestamp'),
    },

    projects = {

        # common info
        u'id': ID(),
        u'manager_id': Integer(required=True, db_references='scientists(id)'),      # person added the project
        u'research_fields': JsonArray(required=True, db_type=''),                   # области науки
        u'title': Text(required=True),                                              # название проекта
        u'description_short': Text(required=True),                                  # краткое описание для обложки
        u'likes': Integer(),                                                        # количество лайков
        u'responses': JsonArray(db_type='json'),                                    # [{scientist_id, vacancy_id}]
        u'university_connection': JsonArray(db_type='json'),                        # [{country, city, university, faculty, chair}]

        # project info
        u'in_progress': Boolean(default=True),                                         # закончен / не закончен
        u'objective': Text(),                                                       # цель исследования
        u'description_full': Text(),                                                # полное описание
        u'usage_possibilities': Text(),                                             # возможности применения результатов
        u'results': Text(),                                                         # достигнутые результаты и практическое применение
        u'related_data': JsonArray(db_type='json'),                                 # [{id, title, project_id, source_link, description}]
        u'leaders': JsonArray(db_type='json'),                                      # [{id, scientist_id, full_name}]
        u'participants': JsonArray(db_type='json'),                                 # [{role_id, role_name, scientist_id, full_name}]
        u'missed_participants': JsonArray(db_type='json'),                          # [{vacancy_id, vacancy_name, description, difficulty}]
        u'tags': JsonArray(db_type='text[]'),                                       # тэги
        u'project_site': Text(),
        u'contacts': JsonArray(db_type='json'),                                     # [{type, id}]

        # system info
        u'dt_created': Datetime(db_type='timestamp'),
    }
)