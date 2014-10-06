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
            objective=u'',
            description_full=u'',
            usage_possibilities=u'',
            results=u'',
            related_data=u'',
            leader=u'',
            participants=[],
            missed_participants=[],
            tags=[],
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