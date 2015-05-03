# -*- coding: utf-8 -*-

import environment

__author__ = 'mayns'


class Project(object):

    project_dict = {
        1: dict(
            id=u'1',
            manager_id=u'2',
            research_fields=[environment.K_MATH, environment.K_BIOLOGY],
            title=u'New Algorithms for Nonnegative Matrix Factorization and Beyond',
            description_short=u'In biology most of the phenomena, whether at the scale of individual development or at '
                              u'that of 'u'Darwinian evolution, are temporally extended. Taking into account repeated '
                              u'iterations and 'u'sequential events is needed for any understanding of the '
                              u'self-organization processes at work in these domains. With two simple examples in plant'
                              u'growth: leaf venation and the formation of the phyllotactic spirals, I will discuss how'
                              u'characteristic structures emerge out of temporally iterated',
            likes=13,
            university_connection=[
                dict(
                    country=u'USA',
                    city=u'Boston',
                    university=u'MIT',
                    faculty=u'biophysics',
                    chair=u'cosy chair'
                )
            ],
            in_progress=u'false',
            objective=u'Surprise!',
            description_full=u'Sed ut perspiciatis, unde omnis iste natus error sit voluptatem accusantium doloremque '
                             u'laudantium, totam rem aperiam eaque ipsa, quae ab illo inventore veritatis et quasi '
                             u'architecto beatae vitae dicta sunt, explicabo. Nemo enim ipsam voluptatem, quia voluptas '
                             u'sit, aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione '
                             u'voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit, '
                             u'amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut '
                             u'labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis '
                             u'nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea '
                             u'commodi consequatur? Quis autem vel eum iure reprehenderit, qui in ea voluptate velit '
                             u'esse, quam nihil molestiae consequatur, vel illum, qui dolorem eum fugiat, quo voluptas '
                             u'nulla pariatur? At vero eos et accusamus et iusto odio dignissimos ducimus, qui '
                             u'blanditiis praesentium voluptatum deleniti atque corrupti, quos dolores et quas '
                             u'molestias excepturi sint, obcaecati cupiditate non provident, similique sunt in culpa, '
                             u'qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem '
                             u'rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est '
                             u'eligendi optio, cumque nihil impedit, quo minus id, quod maxime placeat, facere possimus,'
                             u' omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et '
                             u'aut officiis debitis aut rerum necessitatibus saepe eveniet, ut et voluptates repudiandae '
                             u'sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, '
                             u'ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus '
                             u'asperiores repellat.',
            usage_possibilities=u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor '
                                u'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud '
                                u'exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure '
                                u'dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
                                u' Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt '
                                u'mollit anim id est laborum.',
            results=u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor '
                    u'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud '
                    u'exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure '
                    u'dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. '
                    u'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit '
                    u'anim id est laborum.',
            related_data=[
                dict(
                    id=u'1',
                    title=u'A Bloody Mary, Maria, substitute. Sweet, sour and tart with some heat.',
                    project_id=None,
                    source_link=u'http://www.fireballwhisky.com/recipes/',
                    description=u'officia deserunt mollitia animi, id est laborum et dolorum fuga'
                ),
                dict(
                    id=u'2',
                    title=u'Whoa!',
                    project_id=u'1',
                    source_link=None,
                    description=u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor '
                                u'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud',
                )
            ],
            leader=dict(
                id=u'1',
                scientist_id=u'2',
                full_name=u'K. A.'
            ),
            participants=[
                dict(
                    role_name=u'backend monkey',
                    scientist_id=u'1',
                    first_name=u'Oksana',
                    last_name=u'Gorobets',
                    middle_name=u'V.',
                ),
                dict(
                    role_name=u'DB manager',
                    first_name=u'Dmitry',
                    last_name=u'Makhotin',
                    middle_name=u'V.',
                ),
            ],
            vacancies=[
                dict(
                    vacancy_name=u'Tester',
                    description=u'Functional and Unit Tests',
                    difficulty=8,
                ),
                dict(
                    vacancy_name=u'System Administrator',
                    description=u'Great job for trouble seekers',
                    difficulty=8,
                ),
                dict(
                    vacancy_name=u'A cat',
                    description=u'Just a cat',
                    difficulty=10,
                ),
            ],
            tags=[u'number theory', u'calculations', u'matrices', u'linear algebra'],
            project_site=u'http://math.mit.edu/seminars/lunchseminar/',
            contacts=[
                dict(
                    name=u'Oks',
                    connection=environment.PHONE,
                    number=u'617-253-4359',
                )
            ],
        ),
        2: dict(
            id=u'2',
            manager_id=u'1',
            research_fields=[environment.K_ENGINEERING, environment.K_IT],
            title=u'Измерение тяги в другие страны в зависимости от региона Москвы',
            description_short=u'In biology most of the phenomena, whether at the scale of individual development or at '
                              u'that of 'u'Darwinian evolution, are temporally extended. Taking into account repeated '
                              u'iterations and 'u'sequential events is needed for any understanding of the '
                              u'self-organization processes at work in these domains. With two simple examples in plant'
                              u'growth: leaf venation and the formation of the phyllotactic spirals, I will discuss how'
                              u'characteristic structures emerge out of temporally iterated',
            likes=2,
            university_connection=[
                dict(
                    country=u'РФ',
                    city=u'Москва',
                    university=u'MTI',
                    faculty=u'Обществознание',
                    chair=u'Лаборатория #3'
                )
            ],
            in_progress=u'true',
            objective=u'Surprise!',
            description_full=u'Sed ut perspiciatis, unde omnis iste natus error sit voluptatem accusantium doloremque '
                             u'laudantium, totam rem aperiam eaque ipsa, quae ab illo inventore veritatis et quasi '
                             u'architecto beatae vitae dicta sunt, explicabo. Nemo enim ipsam voluptatem, quia voluptas '
                             u'sit, aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione '
                             u'voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit, '
                             u'amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut '
                             u'labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis '
                             u'nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea '
                             u'commodi consequatur? Quis autem vel eum iure reprehenderit, qui in ea voluptate velit '
                             u'esse, quam nihil molestiae consequatur, vel illum, qui dolorem eum fugiat, quo voluptas '
                             u'nulla pariatur? At vero eos et accusamus et iusto odio dignissimos ducimus, qui '
                             u'blanditiis praesentium voluptatum deleniti atque corrupti, quos dolores et quas '
                             u'molestias excepturi sint, obcaecati cupiditate non provident, similique sunt in culpa, '
                             u'qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem '
                             u'rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est '
                             u'eligendi optio, cumque nihil impedit, quo minus id, quod maxime placeat, facere possimus,'
                             u' omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et '
                             u'aut officiis debitis aut rerum necessitatibus saepe eveniet, ut et voluptates repudiandae '
                             u'sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, '
                             u'ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus '
                             u'asperiores repellat.',
            usage_possibilities=u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor '
                                u'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud '
                                u'exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure '
                                u'dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
                                u' Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt '
                                u'mollit anim id est laborum.',
            results=u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor '
                    u'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud '
                    u'exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure '
                    u'dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. '
                    u'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit '
                    u'anim id est laborum.',
            related_data=[
                dict(
                    id=u'1',
                    title=u'A Bloody Mary, Maria, substitute. Sweet, sour and tart with some heat.',
                    project_id=None,
                    source_link=u'http://www.fireballwhisky.com/recipes/',
                    description=u'officia deserunt mollitia animi, id est laborum et dolorum fuga'
                ),
                dict(
                    id=u'2',
                    title=u'Whoa!',
                    project_id=u'1',
                    source_link=None,
                    description=u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor '
                                u'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud',
                )
            ],
            leader=dict(
                id=u'1',
                scientist_id=u'1',
                full_name=u'Окс'
            ),
            participants=[
                dict(
                    role_name=u'backend monkey',
                    scientist_id=u'1',
                    first_name=u'Oksana',
                    last_name=u'Gorobets',
                    middle_name=u'V.',
                ),
                dict(
                    role_name=u'DB manager',
                    first_name=u'Dmitry',
                    last_name=u'Makhotin',
                    middle_name=u'V.',
                ),
            ],
            vacancies=[
                dict(
                    vacancy_name=u'Tester',
                    description=u'Functional and Unit Tests',
                    difficulty=8,
                ),
                dict(
                    vacancy_name=u'System Administrator',
                    description=u'Great job for trouble seekers',
                    difficulty=8,
                ),
                dict(
                    vacancy_name=u'A cat',
                    description=u'Just a cat',
                    difficulty=10,
                ),
            ],
            tags=[u'number theory', u'calculations', u'matrices', u'linear algebra'],
            project_site=u'http://math.mit.edu/seminars/lunchseminar/',
            contacts=[
                dict(
                    name=u'Oks',
                    connection=environment.PHONE,
                    number=u'617-253-4359',
                )
            ],
        )
    }

    responses = [
        dict(
            scientist_id=u'1',
            project_id=u'1',
            vacancy_id=u'1',
            message=u'Please take me',
            status=environment.STATUS_DECLINED,
        ),
        dict(
            scientist_id=u'1',
            project_id=u'1',
            vacancy_id=u'2',
            message=u'i am the best',
            status=environment.STATUS_WAITING,
        )
    ]

    @classmethod
    def get_project(cls, num=None):
        if not num:
            return cls.project_dict
        return cls.project_dict[num]

    @classmethod
    def get_responses(cls):
        return cls.responses