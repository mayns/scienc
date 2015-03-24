# -*- coding: utf-8 -*-

import logging
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
            scientist_response = dict(
                scientist_id=scientist_id,
                vacancy_id=data[u'vacancy_id'],
                message=data.get(u'message', u'')
            )
            if scientist_response not in project.responses:
                project.responses.append(scientist_response)
                yield project.save(fields=[u'responses'])
                scientist = yield Scientist.get_by_id(scientist_id)
                scientist.desired_vacancies.append(dict(
                    project_id=project.id,
                    vanancy_id=data[u'vacancy_id']
                ))
                yield scientist.save(fields=[u'desired_vacancies'])
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