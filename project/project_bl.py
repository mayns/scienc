# -*- coding: utf-8 -*-

import logging
import environment
import momoko
from tornado import gen

from common.decorators import psql_connection
from common.exceptions import *
from common.utils import generate_id
from db.utils import *

from project.models import Project
from scientist.models import Scientist

__author__ = 'oks'


class ProjectBL(object):
    @classmethod
    @gen.coroutine
    def create(cls, project_dict, test_mode=False):

        participants = project_dict.pop(u'participants', [])
        vacancies = project_dict.pop(u'vacancies', [])

        if not project_dict.get(u'manager_id'):
            raise Exception(u'No manager ID in creating project')

        # create ID
        if test_mode:
            project_id = project_dict.pop(u'id')
        else:
            project_id = generate_id(21)

        editable_data = Project.get_editable_data(project_dict, update=False)
        editable_data.update(id=project_id)
        project = Project(**editable_data)
        yield project.save(update=False, fields=editable_data.keys())

        participant_ids = []
        for participant in participants:
            participant.update(project_id=project_id)
            participant_id = yield cls.update_participants(participant)
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
        participant_id = generate_id(21)
        participant_data.update(id=participant_id)

        sqp_query = get_insert_query(environment.TABLE_PARTICIPANTS, participant_data)
        try:
            yield momoko.Op(conn.execute, sqp_query)
        except PSQLException, ex:
            logging.exception(ex)
        raise gen.Return(participant_id)

    @classmethod
    @gen.coroutine
    @psql_connection
    def update_participant(cls, conn, participant_data):
        sqp_query = get_update_query(environment.TABLE_PARTICIPANTS, participant_data,
                                     where_params=dict(id=participant_data[u'id']))
        try:
            yield momoko.Op(conn.execute, sqp_query)
        except PSQLException, ex:
            logging.exception(ex)
        raise gen.Return(participant_data[u'id'])

    @classmethod
    @gen.coroutine
    @psql_connection
    def delete_participant(cls, conn, participant_id):
        sqp_query = get_delete_query(environment.TABLE_PARTICIPANTS, dict(column=u'id', value=participant_id))
        try:
            yield momoko.Op(conn.execute, sqp_query)
        except PSQLException, ex:
            logging.exception(ex)

    @classmethod
    @gen.coroutine
    @psql_connection
    def add_vacancy(cls, conn, vacancy_data):
        vacancy_id = generate_id(21)
        vacancy_data.update(id=vacancy_id)
        sqp_query = get_insert_query(environment.TABLE_VACANCIES, vacancy_data)
        try:
            yield momoko.Op(conn.execute, sqp_query)
        except PSQLException, ex:
            logging.exception(ex)
        raise gen.Return(vacancy_id)

    @classmethod
    @gen.coroutine
    @psql_connection
    def update_vacancy(cls, conn, vacancy_data):
        sqp_query = get_update_query(environment.TABLE_VACANCIES, vacancy_data,
                                     where_params=dict(id=vacancy_data[u'id']))
        yield momoko.Op(conn.execute, sqp_query)
        try:
            raise gen.Return(vacancy_data[u'id'])
        except PSQLException, ex:
            logging.exception(ex)

    @classmethod
    @gen.coroutine
    @psql_connection
    def delete_vacancy(cls, conn, vacancy_id):
        sqp_query = get_delete_query(environment.TABLE_VACANCIES, dict(column=u'id', value=vacancy_id))
        try:
            yield momoko.Op(conn.execute, sqp_query)
        except PSQLException, ex:
            logging.exception(ex)

    @classmethod
    @gen.coroutine
    def update(cls, project_id, project_dict):

        if not project_id:
            raise Exception(u'No project id provided')

        project = yield Project.get_by_id(project_id)
        updated_data = project.get_updated_data(project_dict)
        if u'vacancies' in updated_data.keys():
            vacancies = updated_data.pop(u'vacancies', [])
            del_vacancy_ids = set(project.vacancies) - set([v[u'id'] for v in vacancies])
            vacancy_ids = []
            for vacancy in vacancies:
                # новые вакансии
                if not vacancy.get(u'id'):
                    vacancy.update(project_id=project_id)
                    v_id = yield cls.add_vacancy(vacancy)

                # ищем те, которые изменились
                elif vacancy.get(u'id') in project.vacancies:
                    v_id = yield cls.update_vacancy(vacancy)

                else:
                    raise Exception(u'Strange vacancy id: {}'.format(vacancy[u'id']))

                vacancy_ids.append(v_id)

            for vacancy_id in del_vacancy_ids:
                yield cls.delete_vacancy(vacancy_id)

            logging.info(u'New ordered vacancies={}; '
                         u'Deleted vacancies={}'.format(vacancy_ids, del_vacancy_ids))
            updated_data.update(vacancies=vacancy_ids)

        if u'participants' in updated_data.keys():
            participants = project_dict.pop(u'participants', [])
            del_participant_ids = set(project.participants) - set([v[u'id'] for v in participants])
            participant_ids = []
            for participant in participants:
                # новые участники
                if not participant.get(u'id'):
                    participant.update(project_id=project_id)
                    p_id = yield cls.add_participant(participant)

                # ищем те, которые изменились
                elif participant.get(u'id') in project.participants:
                    p_id = yield cls.update_participant(participant)

                else:
                    raise Exception(u'Strange participant id: {}'.format(participant[u'id']))

                participant_ids.append(p_id)

            for participant_id in del_participant_ids:
                yield cls.delete_participant(participant_id)

            logging.info(u'New ordered participants={}; '
                         u'Deleted participants={}'.format(participant_ids, del_participant_ids))
            updated_data.update(participants=participant_ids)

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
                project.update(research_fields=
                               [dict(id=f, name=environment.SCIENCE_FIELDS_MAP[f]) for f in project[u'research_fields']])
        raise gen.Return(projects_data)

    @classmethod
    @gen.coroutine
    @psql_connection
    def get_vacancy(cls, conn, v_id):
        # columns = [u'id', u'vacancy_name', u'description', u'difficulty']
        columns = [u'id', u'vacancy_name', u'description']
        sql_query = get_select_query(environment.TABLE_VACANCIES, columns=columns,
                                     where=dict(column=u'id', value=str(v_id)))
        cursor = yield momoko.Op(conn.execute, sql_query)
        data = cursor.fetchone()
        raise gen.Return(dict(zip(columns, data)))

    @classmethod
    @gen.coroutine
    @psql_connection
    def get_participant(cls, conn, p_id):
        columns = [u'id', u'role_name', u'scientist_id', u'first_name', u'middle_name', u'last_name']
        sql_query = get_select_query(environment.TABLE_PARTICIPANTS, columns=columns,
                                     where=dict(column=u'id', value=str(p_id)))
        cursor = yield momoko.Op(conn.execute, sql_query)
        data = cursor.fetchone()
        raise gen.Return(dict(zip(columns, data)))

    @classmethod
    @gen.coroutine
    def get(cls, project_id):
        project_data = yield Project.get_json_by_id(project_id)
        vacancies = []
        participants = []

        for vacancy_id in project_data.get(u'vacancies', []):
            vacancy = yield cls.get_vacancy(vacancy_id)
            vacancies.append(vacancy)
        for p_id in project_data.get(u'participants', []):
            p = yield cls.get_participant(p_id)
            participants.append(p)

        project_data.update(
            vacancies=vacancies,
            participants=participants
        )
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