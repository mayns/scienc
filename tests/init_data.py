# -*- coding: utf-8 -*-

__author__ = 'mayns'


class Scientist(object):

    scientist_dict = {
        0: dict(


            email=u'cooper@gmail.com',
            pwd=u'alice',
            first_name=u'Damn',
            last_name=u'Coffee',
            middle_name=u'Good',
            image_url=u'http://www.gravatar.com/avatar/0feef2db09551df83e7bf61d2d1de25e.png',

        ),

        1: dict(
            email=u'llama@gmail.com',
            pwd=u'alice',
            first_name=u'The Best',
            last_name=u'Pie',
            middle_name=u'Cherry',
            image_url=u'http://www.gravatar.com/avatar/0feef2db09551df83e7bf61d2d1de25e.png',
        )

    }

    @classmethod
    def get_scientist(cls, num=None):
        if not num:
            return cls.scientist_dict
        return cls.scientist_dict[num]