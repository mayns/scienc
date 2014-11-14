# -*- coding: utf-8 -*-

import environment

__author__ = 'mayns'


class TestProject(object):
    projects_list = [
        {
            'id': 1,
            'dt_updated': '12.10.2014',
            'research_fields': 'math',
            'title': 'New Algorithms for Nonnegative Matrix Factorization and Beyond',
            'description_short': 'In biology most of the phenomena, whether at the scale of individual development or at '
                              'that of Darwinian evolution, are temporally extended. Taking into account repeated '
                              'iterations and sequential events is needed for any understanding of the '
                              'self-organization processes at work in these domains. With two simple examples in plant'
                              'growth: leaf venation and the formation of the phyllotactic spirals, I will discuss how'
                              'characteristic structures emerge out of temporally iterated',
            'views': 2,
            'likes': 3,
            'organization': 'MIT, CS lab 1'
        },
        {
            'id': 2,
            'dt_updated': '12.10.2012',
            'research_fields': 'physics',
            'title': 'Hot Spacetimes for Cold Atoms',
            'description_short': 'Building on our earlier work and that of Son, we construct string theory duals of '
                                 'non-relativistic critical phenomena at finite temperature and density. Concretely, '
                                 'we find black hole solutions of type IIB supergravity whose asymptotic geometries '
                                 'realize the Schroedinger group as isometries. We then identify the non-relativistic '
                                 'conformal field theories to which they are dual. We analyze the thermodynamics of '
                                 'these black holes, which turn out to describe the system at finite temperature and '
                                 'finite density. The strong-coupling result for the shear viscosity of the dual '
                                 'non-relativistic field theory saturates the KSS bound.',
            'views': 2,
            'likes': 3,
            'organization': 'MIT, Department of Physics'
        }
    ]

    json_data = {
        1: dict(
            id=1,
            manager=u'',
            research_fields=[environment.MATH],
            title=u'New Algorithms for Nonnegative Matrix Factorization and Beyond',
            description_short=u'In biology most of the phenomena, whether at the scale of individual development or at '
                              u'that of 'u'Darwinian evolution, are temporally extended. Taking into account repeated '
                              u'iterations and 'u'sequential events is needed for any understanding of the '
                              u'self-organization processes at work in these domains. With two simple examples in plant'
                              u'growth: leaf venation and the formation of the phyllotactic spirals, I will discuss how'
                              u'characteristic structures emerge out of temporally iterated',
            views=2,
            likes=3,
            responses=0,
            organization_type=environment.PRIVATE,
            objective=u'In biology most of the phenomena, whether at the scale of individual development or at',
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
            related_data=u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor '
                         u'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud '
                         u'exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure '
                         u'dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. '
                         u'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit '
                         u'anim id est laborum.',
            leader=u'Alexander The Great',
            participants=[
                dict(
                    name=u'Johan Jones',
                    status=u'intern',
                    role=u'programmer'
                ),
                dict(
                    name=u'James Low',
                    status=u'Ph.D',
                    role=u'mathematician'
                )
            ],
            missed_participants=[
                dict(
                    role=u'magician',
                    responsibilities=u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor '
                                     u'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, '
                                     u'quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo '
                                     u'consequat.'
                )
            ],
            tags=[u'number theory', u'calculations', u'matrices', u'linear algebra'],
            contact_manager=u'Jonathan Harmon',
            contacts=[
                dict(
                    id=u'617-253-4359',
                    type=environment.PHONE
                )
            ],
            project_site=u'http://math.mit.edu/seminars/lunchseminar/'
        ),

        2: dict(
            id=2,
            manager=u'',
            research_fields=[environment.PHYSICS, environment.IT],
            title=u'New Algorithms for Nonnegative Matrix Factorization and Beyond',
            description_short=u'In biology most of the phenomena, whether at the scale of individual development or at '
                              u'that of 'u'Darwinian evolution, are temporally extended. Taking into account repeated '
                              u'iterations and 'u'sequential events is needed for any understanding of the '
                              u'self-organization processes at work in these domains. With two simple examples in plant'
                              u'growth: leaf venation and the formation of the phyllotactic spirals, I will discuss how'
                              u'characteristic structures emerge out of temporally iterated',
            views=22,
            likes=31,
            responses=15,
            organization_type=environment.PRIVATE,
            objective=u'In biology most of the phenomena, whether at the scale of individual development or at',
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
            related_data=u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor '
                         u'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud '
                         u'exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure '
                         u'dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. '
                         u'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit '
                         u'anim id est laborum.',
            leader=u'Alexander The Great',
            participants=[
                dict(
                    name=u'Johan Jones',
                    status=u'intern',
                    role=u'programmer'
                ),
            ],
            missed_participants=[
                dict(
                    role=u'magician',
                    responsibilities=u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor '
                                     u'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, '
                                     u'quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo '
                                     u'consequat.'
                )
            ],
            tags=[u'number theory', u'calculations', u'matrices', u'linear algebra'],
            contact_manager=u'Jonathan Harmon',
            contacts=[
                dict(
                    id=u'617-253-4359',
                    type=environment.PHONE
                )
            ],
            project_site=u'http://math.mit.edu/seminars/lunchseminar/'
        ),

        3: dict(

        ),
        4: dict(

        ),
        5: dict(

        ),
        6: dict(

        ),
        7: dict(

        ),
        8: dict(

        ),
        9: dict(

        ),
        10: dict(

        )
    }

    @classmethod
    def get_project(cls, no=1):
        return cls.json_data[no]

    @classmethod
    def get_list_data(cls):
        return cls.projects_list