# -*- coding: utf-8 -*-

import environment

__author__ = 'mayns'


class Project(object):
    json_data = {
        u'1': dict(
            id=u'1',
            manager=u'',
            research_fields=[environment.MATH],
            title=u'New Algorithms for Nonnegative Matrix Factorization and Beyond',
            description_short=u'In biology most of the phenomena, whether at the scale of individual development or at '
                              u'that of 'u'Darwinian evolution, are temporally extended. Taking into account repeated '
                              u'iterations and 'u'sequential events is needed for any understanding of the '
                              u'self-organization processes at work in these domains. With two simple examples in plant'
                              u'growth: leaf venation and the formation of the phyllotactic spirals, I will discuss how'
                              u'characteristic structures emerge out of temporally iterated',
            views=0,
            likes=0,
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

        u'2': dict(

        ),
        u'3': dict(

        ),
        u'4': dict(

        ),
        u'5': dict(

        ),
        u'6': dict(

        ),
        u'7': dict(

        ),
        u'8': dict(

        ),
        u'9': dict(

        ),
        u'10': dict(

        )
    }

    @classmethod
    def get_data(cls):
        return cls.get_data()