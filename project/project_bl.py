# -*- coding: utf-8 -*-

import logging
import environment
from tornado import gen
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
        scientist = yield Scientist.get_by_id(editable_data[u'manager_id'])
        scientist.managing_project_ids.append(project_id)
        yield scientist.save(fields=[u'managing_project_ids'], columns=[u'managing_project_ids'])
        raise gen.Return(dict(id=project_id))

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
            vacancy_name = [v[u'vacancy_name'] for v in project.missed_participants if v[u'id'] == data[u'id']]
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
            excluded_vacancy = [p for p in project.missed_participants if p[u'id'] == data[u'vacancy_id']][0]
            project.missed_participants.remove(excluded_vacancy)

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

            yield project.save(fields=[u'missed_participants', u'participants'],
                               columns=[u'missed_participants', u'participants'])

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