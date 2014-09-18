# -*- coding: utf-8 -*-
import json
import momoko

from tornado import gen
from base.models import PSQLModel, get_insert_sql_query, get_update_sql_query
from common.decorators import psql_connection
import settings

from common.psql_connections import PSQLNonTransactionClient

__author__ = 'oks'


class Project(PSQLModel):

    PSQL_TABLE = u'projects'
    PSQL_COLUMNS = [u'id', u'title', u'objective', u'description', u'results', u'team']

    def __init__(self, project_id):
        super(Project, self).__init__(project_id)
        self.title = u''
        self.objective = u''
        self.description = u''
        self.results = u''
        self.team = u''

    @classmethod
    @gen.coroutine
    def from_db_class_data(cls, project_id, project_dict):
        project = Project(project_id)
        project.title = project_dict.get(u'title', u'')
        project.objective = project_dict.get(u'objective', u'')
        project.description = project_dict.get(u'description', u'')
        project.results = project_dict.get(u'results', u'')
        project.team = project_dict.get(u'team', u'')
        raise gen.Return(project)

    @classmethod
    @gen.coroutine
    @psql_connection()
    def from_db_by_id(cls, conn, project_id):
        cursor = yield momoko.Op(conn.execute, u"SELECT {columns} FROM {table_name} WHERE id={id}".format(columns=u', '.join(cls.PSQL_COLUMNS),
                                                                                                          table_name=cls.PSQL_TABLE,
                                                                                                          id=str(project_id)))
        project_data = cursor.fetchone()
        if not project_data:
            raise gen.Return((None, None))
        json_project = dict(zip(cls.PSQL_COLUMNS, project_data))
        project = yield cls.from_db_class_data(project_id, json_project)
        raise gen.Return((project, json_project))


    @classmethod
    @gen.coroutine
    @psql_connection()
    def get_all_json(cls, conn):
        cursor = yield momoko.Op(conn.execute, u'SELECT * FROM {table_name}'.format(table_name=cls.PSQL_TABLE))
        projects_data = cursor.fetchall()
        if not projects_data:
            raise gen.Return(None)
        json_projects = json.dumps({'project': [dict(zip(cls.PSQL_COLUMNS, project_data)) for project_data in projects_data]})
        raise gen.Return(json_projects)


    @gen.coroutine
    def save(self, update=True):
        conn = PSQLNonTransactionClient.get_client(partition=settings.PSQL_PARTITION_DEFAULT)
        update_params = dict(
            id=self.id,
            title=self.title,
            description=self.description,
            objective=self.objective,
            results=self.results,
            team=self.team
        )
        if update:
            sqp_query, params = get_update_sql_query(self.psql_table, update_params, dict(id=self.id))
        else:
            update_params.update(dict(id=self.id))
            sqp_query, params = get_insert_sql_query(self.psql_table, update_params)
        yield momoko.Op(conn.execute, sqp_query, params)
