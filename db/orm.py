# -*- coding: utf-8 -*-

from common.descriptors import *

__author__ = 'mayns'


MODELS = dict(
    scientists={

        # common info
        u'id': ID(db_references='roles(id)'),
        u'email': Text(required=True, length=20),
        u'first_name': Text(required=True, length=20),
        u'last_name': Text(required=True, length=20),
        u'middle_name': Text(length=20),
        u'dob': Datetime(db_type='date'),
        u'gender': Text(length=1),
        u'image_url': Text(length=0),
        u'location': JsonObject(),                                                  # {country, city}

        # professional info
        u'middle_education': JsonObject(),                                          # {country, city, school, graduation_year}
        u'high_education': JsonArray(db_type='json'),                               # [{country, city, university, faculty, chair, degree, graduation_year}]
        u'publications': JsonArray(db_type='json'),                                 # [{id, title, source, year, link}]
        u'interests': JsonArray(db_type='text[]'),
        u'about': Text(length=300),
        u'contacts': JsonArray(db_type='json'),                                     # [{connection, number}]

        # app activity
        u'participating_projects': JsonArray(db_type='json'),                       # [{project_id, role_id}]
        u'liked_projects': JsonArray(db_type='bigint[]'),                           # [project_id]
        u'desired_vacancies': JsonArray(db_type='json'),                            # [{project_id, vacancy_id}]
        u'managing_project_ids': JsonArray(db_type='bigint[]'),
        u'achievements': JsonArray(db_type='bigint[]'),                             # [achievement_id]

        # system info
        u'dt_created': Datetime(db_type='timestamp'),
    },

    projects={

        # common info
        u'id': ID(),
        u'manager_id': Integer(required=True, db_references='scientists(id)'),      # person added the project
        u'research_fields': JsonArray(required=True),                               # области науки
        u'title': Text(required=True),                                              # название проекта
        u'description_short': Text(required=True),                                  # краткое описание для обложки
        u'likes': Integer(),                                                        # количество лайков
        u'responses': JsonArray(db_type='jsonb'),                                   # [{scientist_id, vacancy_id, message}]
        u'university_connection': JsonArray(db_type='jsonb'),                       # [{country, city, university, faculty, chair}]

        # project info
        u'in_progress': Text(default=u'true'),                                      # закончен / не закончен
        u'objective': Text(length=300),                                             # цель исследования
        u'description_full': Text(length=300),                                      # полное описание
        u'usage_possibilities': Text(length=300),                                   # возможности применения результатов
        u'results': Text(length=300),                                               # достигнутые результаты и практическое применение
        u'related_data': JsonArray(db_type='jsonb'),                                # [{id, title, project_id, source_link, description}]
        u'leader': JsonObject(),                                                    # [{id, scientist_id, full_name}]
        u'participants': JsonArray(db_type='jsonb'),                                # [{role_id, role_name, scientist_id, full_name}]
        u'missed_participants': JsonArray(db_type='jsonb'),                         # [{vacancy_id, vacancy_name, description, difficulty}]
        u'tags': JsonArray(db_type='text[]'),                                       # тэги
        u'project_site': Text(length=20),
        u'contacts': JsonArray(db_type='jsonb'),                                    # [{name, connection, number}]

        # system info
        u'title_tsvector': TSvector(),                                              # лексемы названия
        u'description_short_tsvector': TSvector(),                                  # лексемы краткого описания
        u'dt_created': Datetime(db_type='timestamp'),
    },


    vacancies = {
        u'id': ID(),
        u'project_id': Integer(required=True, db_references='projects(id)'),
        u'vacancy_name': Text(),
        u'vacancy_name_tsvector': TSvector(),
        u'description': Text(),
        u'vacancy_description_tsvector': TSvector(),
        u'difficulty': Text()
    }
)