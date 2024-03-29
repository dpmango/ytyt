from collections import OrderedDict
from django.db.models import Q


CONFIG = OrderedDict({
    'passing_speed_report': OrderedDict({
        'meta': {
            'ru': 'Отчет о скорости прохождения курса',
            'query': Q(is_staff=False),
        },
        'mapping': [
            {
                'title': 'ФИО',
                'value': lambda user: user.fio,
                'set_column_auto_width': True,
            },
            {
                'title': 'Email',
                'value': lambda user: user.email,
                'set_column_auto_width': True,
            },
            {
                'title': 'Оплатил/не оплатил',
                'value': 'fact_of_payment',
                'set_column_auto_width': True,
            },
            {
                'title': 'Дата регистрации',
                'value': lambda user: user.date_joined.strftime('%d-%m-%Y'),
                'set_column_auto_width': True,
            },
            {
                'title': 'Дата оплаты',
                'value': 'date_payment',
                'set_column_auto_width': True,
            },
        ]
    }),

    'users_report': OrderedDict({
        'meta': {
            'ru': 'Отчет о студентах',
            'query': Q(is_staff=False),
        },
        'mapping': [
            {
                'title': 'ФИО',
                'value': lambda user: user.fio,
                'set_column_auto_width': True,
            },
            {
                'title': 'Email',
                'value': lambda user: user.email,
                'set_column_auto_width': True,
            },
            {
                'title': 'Оплатил/не оплатил',
                'value': 'fact_of_payment',
                'set_column_auto_width': True,
            },
            {
                'title': 'Дата регистрации',
                'value': lambda user: user.date_joined.strftime('%d-%m-%Y'),
                'set_column_auto_width': True,
            },
            {
                'title': 'Дата оплаты',
                'value': 'date_payment',
                'set_column_auto_width': True,
            },
            {
                'title': 'Последний пройденный урок',
                'value': 'last_lesson_completed',
                'set_column_auto_width': True,
            },
            {
                'title': 'Назначенный ментор',
                'value': lambda user: user.reviewer.email if user.reviewer else None,
                'set_column_auto_width': True,
            },
            {
                'title': 'Количество сообщений ревьюеру',
                'value': lambda user: user.dialogmessage_set.count(),
                'set_column_auto_width': True,
            },
        ]
    }),

    'reviewers_report': OrderedDict({
        'meta': {
            'ru': 'Отчет о менторах',
            'query': Q(is_staff=True),
        },
        'mapping': [
            {
                'title': 'ФИО',
                'value': lambda reviewer: reviewer.fio,
                'set_column_auto_width': True,
            },
            {
                'title': 'Email',
                'value': lambda reviewer: reviewer.email,
                'set_column_auto_width': True,
            },
            {
                'title': 'Дата регистрации',
                'value': lambda user: user.date_joined.strftime('%d-%m-%Y'),
                'set_column_auto_width': True,
            },
            {
                'title': 'Количество активных студентов',
                'value': lambda reviewer: reviewer.user_set.count(),
                'set_column_auto_width': True,
            },
            {
                'title': 'Количество сообщений',
                'value': lambda reviewer: reviewer.dialogmessage_set.count(),
                'set_column_auto_width': True,
            },
            {
                'title': 'Среднее время ответа на вопрос (минут)',
                'value': 'average_time_answer',
                'set_column_auto_width': True,
            },
        ]
    }),
})
