# -*- coding: utf-8 -*-

from common.descriptors import *

__author__ = 'mayns'


MODELS = dict(
    scientists={

        # common info
        u'id': ID(db_references='roles(id)', u_editable=False),
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
        u'participating_projects': JsonArray(db_type='json', u_editable=False),     # [{project_id, role_id}]
        u'liked_projects': JsonArray(db_type='bigint[]', u_editable=False),         # [project_id]
        u'desired_vacancies': JsonArray(db_type='json', u_editable=False),          # [{project_id, vacancy_id}]
        u'managing_project_ids': JsonArray(db_type='bigint[]', u_editable=False),
        u'achievements': JsonArray(db_type='bigint[]', u_editable=False),           # [achievement_id]

        # system info
        u'dt_created': Datetime(db_type='timestamp', u_editable=False),
    },

    projects={

        # common info
        u'id': ID(u_editable=False),
        u'manager_id': Integer(required=True, db_references='scientists(id)',
                               u_editable=False),                                   # person added the project
        u'research_fields': JsonArray(required=True, db_type=''),                   # области науки
        u'title': Text(required=True),                                              # название проекта
        u'title_tsvector': TSvector(u_editable=False),                              # лексемы названия
        u'description_short': Text(required=True),                                  # краткое описание для обложки
        u'description_short_tsvector': TSvector(),                                  # лексемы краткого описания
        u'likes': Integer(u_editable=False),                                        # количество лайков
        u'responses': JsonArray(db_type='jsonb', u_editable=False),                 # [{scientist_id, vacancy_id}]
        u'university_connection': JsonArray(db_type='jsonb'),                       # [{country, city, university, faculty, chair}]

        # project info
        u'in_progress': Boolean(default=True),                                      # закончен / не закончен
        u'objective': Text(),                                                       # цель исследования
        u'description_full': Text(),                                                # полное описание
        u'usage_possibilities': Text(),                                             # возможности применения результатов
        u'results': Text(),                                                         # достигнутые результаты и практическое применение
        u'related_data': JsonArray(db_type='jsonb'),                                # [{id, title, project_id, source_link, description}]
        u'leaders': JsonObject(),                                                   # [{id, scientist_id, full_name}]
        u'participants': JsonArray(db_type='jsonb'),                                # [{role_id, role_name, scientist_id, full_name}]
        u'missed_participants': JsonArray(db_type='jsonb'),                         # [{vacancy_id, vacancy_name, description, difficulty}]
        u'tags': JsonArray(db_type='text[]'),                                       # тэги
        u'project_site': Text(),
        u'contacts': JsonArray(db_type='jsonb'),                                    # [{type, id}]

        # system info
        u'dt_created': Datetime(db_type='timestamp', u_editable=False),
    }
)