# -*- coding: utf-8 -*-

import logging
import globals
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
        """
        Добавить участника в таблицу участников
        :param conn:
        :param participant_data: {project_id, role_name, scientist_id, first_name, last_name, middle_name}
        :type participant_data: dict
        """
        participant_id = generate_id(21)
        participant_data.update(id=participant_id)

        sql_query = get_insert_query(globals.TABLE_PARTICIPANTS, participant_data)
        try:
            yield momoko.Op(conn.execute, sql_query)
        except PSQLException, ex:
            logging.exception(ex)
        raise gen.Return(participant_id)

    @classmethod
    @gen.coroutine
    @psql_connection
    def update_participant(cls, conn, participant_data):
        sqp_query = get_update_query(globals.TABLE_PARTICIPANTS, participant_data,
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
        sqp_query = get_delete_query(globals.TABLE_PARTICIPANTS, dict(column=u'id', value=participant_id))
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
        sqp_query = get_insert_query(globals.TABLE_VACANCIES, vacancy_data)
        try:
            yield momoko.Op(conn.execute, sqp_query)
        except PSQLException, ex:
            logging.exception(ex)
        raise gen.Return(vacancy_id)

    @classmethod
    @gen.coroutine
    @psql_connection
    def update_vacancy(cls, conn, vacancy_data):
        sqp_query = get_update_query(globals.TABLE_VACANCIES, vacancy_data,
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
        sqp_query = get_delete_query(globals.TABLE_VACANCIES, dict(column=u'id', value=vacancy_id))
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
            project_v_ids = [v[u'id'] for v in project.vacancies]
            del_vacancy_ids = set(project_v_ids) - set([v[u'id'] for v in vacancies if u'id' in v])
            vacancy_ids = []
            for vacancy in vacancies:
                # новые вакансии
                if not vacancy.get(u'id'):
                    vacancy.update(project_id=project_id)
                    v_id = yield cls.add_vacancy(vacancy)

                # ищем те, которые изменились
                elif vacancy.get(u'id') in project_v_ids:
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
            project_p_ids = [v[u'id'] for v in project.participants]
            del_participant_ids = set(project_p_ids) - set([p[u'id'] for p in participants if u'id' in p])
            participant_ids = []
            for participant in participants:
                # новые участники
                if not participant.get(u'id'):
                    participant.update(project_id=project_id)
                    p_id = yield cls.add_participant(participant)

                # ищем те, которые изменились
                elif participant.get(u'id') in project_p_ids:
                    p_id = yield cls.update_participant(participant)

                else:
                    raise Exception(u'Strange participant id: {}'.format(participant[u'id']))

                participant_ids.append(p_id)

            for participant_id in del_participant_ids:
                yield cls.delete_participant(participant_id)

            logging.info(u'New ordered participants={}; '
                         u'Deleted participants={}'.format(participant_ids, list(del_participant_ids)))
            updated_data.update(participants=participant_ids)

        project.populate_fields(updated_data)

        if updated_data.keys():
            yield project.save(fields=updated_data.keys())

        raise gen.Return(dict(project_id=project_id))

    @classmethod
    @gen.coroutine
    def delete(cls, project_id):
        """
        Удалить участников, удалить вакансии, поставить статус откликам - удаленные.
        У ученого убрать из managing_project_ids.
        """
        project = yield Project.get_by_id(project_id)
        for participant_id in project.participants:
            yield cls.delete_participant(participant_id)
        for vacancy_id in project.vacancies:
            yield cls.delete_vacancy(vacancy_id)
        for response_id in project.responses:
            yield cls.set_del_status_response(response_id)
        scientist = yield Scientist.get_by_id(project.manager_id)
        scientist.managing_project_ids.remove(project_id)
        yield scientist.save(fields=[u'managing_project_ids'], columns=[u'managing_project_ids'])
        yield Project.delete(project_id, tbl=Project.TABLE)

    @classmethod
    @gen.coroutine
    def get_all(cls, columns=None):
        if not columns:
            columns = Project.OVERVIEW_FIELDS
        projects_data = yield Project.get_all_json(columns=columns)
        for project in projects_data:
            if u'research_fields' in project:
                project.update(research_fields=
                               [dict(id=f, name=globals.SCIENCE_FIELDS_MAP[f]) for f in project[u'research_fields']
                                if f in globals.SCIENCE_FIELDS_MAP])
        raise gen.Return(projects_data)

    @classmethod
    @gen.coroutine
    @psql_connection
    def get_vacancy(cls, conn, v_id):
        # columns = [u'id', u'vacancy_name', u'description', u'difficulty']
        columns = [u'id', u'vacancy_name', u'description']
        sql_query = get_select_query(globals.TABLE_VACANCIES, columns=columns,
                                     where=dict(column=u'id', value=str(v_id)))
        cursor = yield momoko.Op(conn.execute, sql_query)
        data = cursor.fetchone()
        zipper = {k[0]: k[1] for k in zip(columns, data) if k[1]}
        raise gen.Return(zipper)

    @classmethod
    @gen.coroutine
    @psql_connection
    def get_participant(cls, conn, p_id):
        columns = [u'id', u'role_name', u'scientist_id', u'first_name', u'middle_name', u'last_name']
        sql_query = get_select_query(globals.TABLE_PARTICIPANTS, columns=columns,
                                     where=dict(column=u'id', value=str(p_id)))
        cursor = yield momoko.Op(conn.execute, sql_query)
        data = cursor.fetchone()
        zipper = {k[0]: k[1] for k in zip(columns, data) if k[1]}
        raise gen.Return(zipper)

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
    @psql_connection
    def add_response(cls, conn, data):
        """
        Участник нажимает кнопку "Участвовать" у проекта. Добавляем втаблицу откликов новое значение.
        Прописываем отклик у ученого и у проекта.
        :param data: {scientist_id, project_id, vacancy_id, message}
        :type data: dict
        """
        project = yield Project.get_by_id(data[u'project_id'])
        scientist = yield Scientist.get_by_id(data[u'scientist_id'])
        sql_query = get_insert_query(globals.TABLE_RESPONSES, data, returning=u'')
        print sql_query
        try:
            yield momoko.Op(conn.execute, sql_query)
        except PSQLException, ex:
            logging.exception(ex)
            raise
        response_id = u'{}:{}:{}'.format(data[u'scientist_id'], data[u'project_id'], data[u'vacancy_id'])
        scientist.desired_vacancies += [response_id]
        project.responses += [response_id]
        yield scientist.save(fields=[u'desired_vacancies'], columns=[u'desired_vacancies'])
        yield project.save(fields=[u'responses'], columns=[u'responses'])

    @classmethod
    @gen.coroutine
    @psql_connection
    def update_response(cls, conn, data):
        """
        Принять, отклонить. Решает менеджер проекта.
        Обновляется статус в самом отклике. Если статус == Принять,
        участник добавляется в участники проекта с ролью в виде названия вакансии.
        Вакансия не удаляется на случай, если нужно несколько участников.
        Другим участникам также ничего не прислыается.
        Можно отправить Отклонить всех со страницы Мои проекты.

        :param data: {scientist_id, project_id, vacancy_id, result}
        :type data: dict
        """
        sql_query = get_update_query(globals.TABLE_RESPONSES, dict(status=data[u'result']),
                                     where_params=dict(scientist_id=data[u'scientist_id'],
                                                       project_id=data[u'project_id'],
                                                       vacancy_id=data[u'vacancy_id']), returning=u'')
        try:
            yield momoko.Op(conn.execute, sql_query)
        except PSQLException, ex:
            logging.exception(ex)

        if data[u'result'] == globals.STATUS_ACCEPTED:

            sql_query = get_select_query(globals.TABLE_VACANCIES, columns=[u'vacancy_name'],
                                            where=dict(column=u'id', value=data[u'vacancy_id']))
            cursor = yield momoko.Op(conn.execute, sql_query)
            vacancy_name = cursor.fetchone()[0]

            scientist = yield Scientist.get_by_id(data[u'scientist_id'])
            participant_data = dict(
                project_id=data[u'project_id'],
                scientist_id=data[u'scientist_id'],
                role_name=vacancy_name,
                first_name=scientist.first_name.decode('utf-8') if isinstance(scientist.first_name, str) else scientist.first_name,
                last_name=scientist.last_name.decode('utf-8') if isinstance(scientist.last_name, str) else scientist.last_name,
                middle_name=scientist.middle_name.decode('utf-8') if isinstance(scientist.middle_name, str) else scientist.middle_name,
            )
            project = yield Project.get_by_id(data[u'project_id'])
            participant_id = yield cls.add_participant(participant_data)
            project.participants = [p[u'id'] for p in project.participants] + [participant_id]
            yield project.save(fields=[u'participants'], columns=[u'participants'])

    @classmethod
    @gen.coroutine
    def delete_response(cls, response_id):
        pass

    @classmethod
    @gen.coroutine
    @psql_connection
    def set_del_status_response(cls, conn, response_id):
        sc_id, p_id, v_id = response_id.split(u':')
        sql_query = get_update_query(globals.TABLE_RESPONSES, dict(status=globals.STATUS_DELETED),
                                     where_params=dict(scientist_id=sc_id,
                                                       project_id=p_id,
                                                       vacancy_id=v_id))
        try:
            yield momoko.Op(conn.execute, sql_query)
        except PSQLException, ex:
            logging.exception(ex)

    @classmethod
    @gen.coroutine
    def search_projects(cls, data):
        pass