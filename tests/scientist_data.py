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
            image_url=u'',
            dob=u'1986-10-13',
            liked_projects=[1],

        ),

        1: dict(
            email=u'llama@gmail.com',
            pwd=u'alice',
            first_name=u'The Best',
            last_name=u'Pie',
            middle_name=u'Cherry',
            dob=u'1986-10-13',
            image_url=u'',
        ),

        2: dict(
            email=u'oksgorobets@gmail.com',
            pwd=u'alice',
            first_name=u'Оксана',
            last_name=u'Горобец',
            middle_name=u'Валерьевна',
            dob=u'1986-10-13',
            gender=u'f',
            location={u'country': u'Russia', u'city': u'Moscow'},
            image_url=u'https://en.gravatar.com/userimage/39116033/0b1c1ef31de9d584943a47db3a03143a.jpg',
            middle_education=dict(
                country=u'Россия',
                city=u'Тверь',
                school=u'Гимназия 8',
                graduation_year=u'2004'
            ),
            high_education=[
                dict(
                    country=u'Россия',
                    city=u'Тверь',
                    university=u'ТвГУ',
                    faculty=u'Филологический',
                    chair=u'Издательское дело и редактирование',
                    degree=u'специалист',
                    graduation_year=u'2011'
                ),
                dict(
                    country=u'Россия',
                    city=u'Москва',
                    university=u'МГУ им. Ломоносова',
                    faculty=u'ВМиК',
                    chair=u'ПМ и ПО',
                    degree=u'bachelor',
                    graduation_year=u'2015'
                )
            ],
            publications=[
                dict(
                    title=u'How I stopped procrastinating ',
                    source=u'I did NOT!',
                    year=2004,
                    link=u'http://geektimes.ru/post/166369/'
                )
            ],
            interests=[u'лингвистика', u'искусственный интеллект', u'алгоритмы'],
            about=u'Oh, Enough!',

            contacts=[
                dict(
                    connection=u'Phone',
                    number=u'89104714456'
                ),
                dict(
                    connection=u'email',
                    number=u'ifine13@gmail.com'
                ),
                dict(
                    connection=u'Skype',
                    number=u'leff_mayns'
                ),
                dict(
                    connection=u'Instagram',
                    number=u'@leff_mayns'
                )
            ],

            liked_projects=[1],

            participating_projects=[
                dict(
                    project_id=0,
                    role_id=0
                ),

                dict(
                    project_id=1,
                    role_id=0
                )
            ],
            desired_vacancies=[
                dict(
                    project_id=666,
                    vacancy_id=0
                )
            ],
            managing_project_ids=[0, 1],

            achievements=[0],
        ),

        3: dict(
            email=u'losogudok@yandex.ru',
            pwd=u'qwe',
            first_name=u'Андрей',
            last_name=u'Костин',
            middle_name=u'Васильевич',
            dob=u'1989-12-19',
            gender=u'm',
            location={u'country': u'Russia', u'city': u'Moscow'},
            image_url=u'https://en.gravatar.com/userimage/39116033/0b1c1ef31de9d584943a47db3a03143a.jpg',
            middle_education=dict(
                country=u'Россия',
                city=u'Москва',
                school=u'Гимназия 1551',
                graduation_year=u'2007'
            ),
            high_education=[
                dict(
                    country=u'Россия',
                    city=u'Москва',
                    university=u'МГУ им. Ломоносова',
                    faculty=u'Психологии',
                    chair=u'Общая психология',
                    degree=u'bachelor',
                    graduation_year=u'2012'
                ),
                dict(
                    country=u'Россия',
                    city=u'Москва',
                    university=u'МГУ им. Ломоносова',
                    faculty=u'Экономики',
                    chair=u'Агроэкономики',
                    degree=u'магистр',
                    graduation_year=u'2015'
                )
            ],
            publications=[
                dict(
                    title=u'Корпускулярно-кинетическая теория',
                    source=u'Питер',
                    year=2012,
                    link=u'https://www.rsl.ru/datadocs/doc_4677je.pdf'
                )
            ],
            interests=[u'javasript', u'nodejs', u'60fps'],
            about=u'Я вообще парень огого!',

            contacts=[
                dict(
                    connection=u'Phone',
                    number=u'89263031827'
                ),
                dict(
                    connection=u'email',
                    number=u'losogudok@yandex.ru'
                ),
                dict(
                    connection=u'Skype',
                    number=u'losogudok'
                )
            ],

            liked_projects=[1],

            participating_projects=[
                dict(
                    project_id=0,
                    role_id=1
                ),

                dict(
                    project_id=1,
                    role_id=1
                )
            ],
            desired_vacancies=[
                dict(
                    project_id=666,
                    vacancy_id=1
                )
            ],
            managing_project_ids=[1],

            achievements=[0],
        )

    }

    @classmethod
    def get_scientist(cls, num=None):
        if not num:
            return cls.scientist_dict
        return cls.scientist_dict[num]