# -*- coding: utf-8 -*-

import logging
import environment
import momoko
from tornado import gen

from common.decorators import psql_connection
from common.exceptions import *
from db.utils import *

from project.models import Project
from scientist.models import Scientist

__author__ = 'oks'


class ProjectBL(object):
    @classmethod
    @gen.coroutine
    def create(cls, project_dict):

        editable_data = Project.get_editable_data(project_dict, update=False)
        project = Project(**editable_data)
        project_id = yield project.save(update=False, fields=editable_data.keys())

        participant_ids = []
        participants = editable_data.pop(u'participants', [])
        vacancies = editable_data.pop(u'vacancies', [])
        for participant in participants:
            participant.update(project_id=project_id)
            participant_id = yield cls.add_participant(participant)
            participant_ids.append(participant_id)

        vacancy_ids = []
        for vacancy in vacancies:
            vacancy.update(project_id=project_id)
            v_id = yield cls.add_vacancy(vacancy)
            vacancy_ids.append(v_id)

        project.participants = participant_ids
        project.vacancies = vacancy_ids
        yield project.save(fields=[u'participants', u'vacancies'])

        scientist = yield Scientist.get_by_id(editable_data[u'manager_id'])
        scientist.managing_project_ids.append(project_id)
        yield scientist.save(fields=[u'managing_project_ids'], columns=[u'managing_project_ids'])
        raise gen.Return(dict(id=project_id))

    @classmethod
    @gen.coroutine
    @psql_connection
    def add_participant(cls, conn, participant_data):
        participant_id = 0
        sqp_query = get_insert_query(environment.TABLE_PARTICIPANTS, participant_data)
        try:
            cursor = yield momoko.Op(conn.execute, sqp_query)
            participant_id = cursor.fetchone()[0]
        except PSQLException, ex:
            print ex

        raise gen.Return(participant_id)

    @classmethod
    @gen.coroutine
    @psql_connection
    def add_vacancy(cls, conn, vacancy_data):
        vacancy_id = 0
        sqp_query = get_insert_query(environment.TABLE_VACANCIES, vacancy_data)
        try:
            cursor = yield momoko.Op(conn.execute, sqp_query)
            vacancy_id = cursor.fetchone()[0]
        except PSQLException, ex:
            print ex

        raise gen.Return(vacancy_id)

    @classmethod
    @gen.coroutine
    def update(cls, project_id, project_dict):

        if not project_id:
            raise Exception(u'No project id provided')

        project = yield Project.get_by_id(project_id)
        updated_data = project.get_updated_data(project_dict)
        project.populate_fields(updated_data)

        yield project.save(fields=updated_data.keys())
        raise gen.Return(dict(project_id=project_id))

    @classmethod
    @gen.coroutine
    def delete(cls, project_id):
        yield Project.delete(project_id, tbl=Project.TABLE)

    @classmethod
    @gen.coroutine
    def get_all(cls):
        projects_data = yield Project.get_all_json(columns=Project.OVERVIEW_FIELDS)
        for project in projects_data:
            if u'research_fields' in project:
                project.update(research_fields=[dict(id=f, name=environment.SCIENCE_FIELDS_MAP[f]) for f in project[u'research_fields']])
        raise gen.Return(projects_data)

    @classmethod
    @gen.coroutine
    def get(cls, project_id):
        project_data = yield Project.get_json_by_id(project_id)
        raise gen.Return(project_data)

    @classmethod
    @gen.coroutine
    def add_like(cls, project_id, scientist_id):
        project = yield Project.get_by_id(project_id)
        project.likes += 1
        scientist = yield Scientist.get_by_id(scientist_id)
        scientist.liked_projects = list(set(scientist.liked_projects.append(project_id)))
        yield project.save(fields=['likes'])
        yield scientist.save(fields=['liked_projects'])

    @classmethod
    @gen.coroutine
    def delete_like(cls, project_id, scientist_id):
        project = yield Project.get_by_id(project_id)
        project.likes -= 1
        scientist = yield Scientist.get_by_id(scientist_id)
        scientist.liked_projects.remove(project_id)
        yield project.save(fields=['likes'])
        yield scientist.save(fields=['liked_projects'])

    @classmethod
    @gen.coroutine
    def add_participation(cls, data):
        # message, scientist_id, vacancy_id, project_id
        scientist_id = data[u'scientist_id']
        try:
            project = yield Project.get_by_id(data[u'project_id'])
            vacancy_name = [v[u'vacancy_name'] for v in project.vacancies if v[u'id'] == data[u'id']]
            if not vacancy_name:
                raise Exception(u'No vacancy name')
            scientist_response = dict(
                scientist_id=scientist_id,
                vacancy_id=data[u'id'],
                vacancy_name=vacancy_name[0],
                message=data.get(u'message', u'')
            )
            if scientist_response not in project.responses:
                project.responses.append(scientist_response)
                yield project.save(fields=[u'responses'], columns=[u'responses'])
                scientist = yield Scientist.get_by_id(scientist_id)
                scientist.desired_vacancies = scientist.desired_vacancies or []
                scientist.desired_vacancies.append(dict(
                    project_id=project.id,
                    vacancy_id=data[u'id']
                ))
                yield scientist.save(fields=[u'desired_vacancies'], columns=[u'desired_vacancies'])
        except Exception, ex:
            logging.exception(ex)


    @classmethod
    @gen.coroutine
    def delete_participation(cls, data):
        # scientist_id, project_id
        scientist_id = data[u'scientist_id']
        try:
            project = yield Project.get_by_id(data[u'project_id'])
            project.responses = [sc for sc in project.responses if sc[u'scientist_id'] != scientist_id]
            yield project.save(fields=[u'responses'])

            scientist = yield Scientist.get_by_id(scientist_id)
            scientist.desired_vacancies = [v for v in scientist.desired_vacancies if v[u'project_id'] != project.id]

            yield scientist.save(fields=[u'desired_vacancies'])
        except Exception, ex:
            logging.exception(ex)

    @classmethod
    @gen.coroutine
    def accept_response(cls, data):
        """

        :param data: {scientist_id, project_id, vacancy_id}
        :type data: dict

        """
        try:
            project = yield Project.get_by_id(data[u'project_id'])
            scientist = yield Scientist.get_by_id(data[u'scientist_id'])
            excluded_vacancy = [p for p in project.vacancies if p[u'id'] == data[u'vacancy_id']][0]
            project.vacancies.remove(excluded_vacancy)

            project.participants.append(dict(
                full_name=u' '.join(map(lambda x: x.decode('utf8'), [scientist.last_name, scientist.first_name,
                                                                     scientist.middle_name])),
                scientist_id=data[u'scientist_id'],
                role_name=excluded_vacancy[u'vacancy_name']
            ))
            desired_vacancy = [v for v in scientist.desired_vacancies if v[u'vacancy_id'] == data[u'vacancy_id']][0]

            for v in scientist.desired_vacancies:
                if v[u'vacancy_id'] != data[u'vacancy_id']:
                    continue
                v[u'status'] = environment.STATUS_ACCEPTED

            scientist.participating_projects.append(dict(
                project_id=desired_vacancy[u'project_id'],
                role_id=desired_vacancy[u'vacancy_id']
            ))

            yield project.save(fields=[u'vacancies', u'participants'],
                               columns=[u'vacancies', u'participants'])

            yield scientist.save(fields=[u'desired_vacancies', u'participating_projects'],
                                 columns=[u'desired_vacancies', u'participating_projects'])
        except Exception, ex:
            logging.exception(ex)

    @classmethod
    @gen.coroutine
    def decline_response(cls, data):
        try:
            scientist = yield Scientist.get_by_id(data[u'scientist_id'])
            for v in scientist.desired_vacancies:
                if v[u'vacancy_id'] != data[u'vacancy_id']:
                    continue
                v[u'status'] = environment.STATUS_DECLINED
            yield scientist.save(fields=[u'desired_vacancies'], columns=[u'desired_vacancies'])
        except Exception, ex:
            logging.exception(ex)

    @classmethod
    @gen.coroutine
    def search_projects(cls, data):
        pass