GROUP_ADMINISTRATOR = 1
GROUP_REVIEWER = 2
GROUP_STUDENT = 3

GROUPS = (
    (GROUP_ADMINISTRATOR, 'Администратор'),
    (GROUP_REVIEWER, 'Ревьюер'),
    (GROUP_STUDENT, 'Студент'),
)

GROUPS_DESCRIPTION = (
    (GROUP_ADMINISTRATOR, ''),
    (GROUP_REVIEWER, ''),
    (GROUP_STUDENT, '')
)

GROUP_RIGHTS = {}

"""
Список доступных прав, возможности:
- permissions.login – вход в систему

- permissions.system.settings – менять настройки системы

- permissions.common.search – искать в системе что-либо
 
– permissions.users.index – просматривать пользователей
– permissions.users.edit – редактировать пользователей

- permissions.profile.index - просматривать свой профиль
- permissions.profile.edit - редактировать свой профиль 

- permissions.subjects.index - просматривать тематики обращений
- permissions.subjects.edit - редактировать тематики обращений

- permissions.links.index - просматривать полезные ссылки
- permissions.links.edit - редактировать полезные ссылки

- permissions.clients.index - просматривать клиентов
- permissions.clients.edit - редактировать клиентов 
- permissions.clients.card-activation - аткивировать карту

- permissions.files.upload - загружать файлы
- permissions.files.edit - изменять файлы (удалять)

- permissions.product_categories.index - просматривать раздел категорий ЛП
- permissions.product_categories.edit - изменять раздел категорий ЛП
"""

GROUP_RIGHTS[GROUP_ADMINISTRATOR] = [
    'permissions.admin.index',
    'permissions.admin.@superuser',

    'permissions.users.index',
    'permissions.users.edit',

    'permissions.profile.index',
    'permissions.profile.edit',

    'permissions.subjects.index',
    'permissions.subjects.@admin',
    'permissions.subjects.edit',


    'permissions.clients.index',
    'permissions.clients.edit',
    'permissions.clients.card-activation',

    'permissions.files.upload',
    'permissions.files.edit',

    'permissions.product_categories.index',
    'permissions.product_categories.edit',

    'permissions.search.index',
]

GROUP_RIGHTS[GROUP_REVIEWER] = [
    'permissions.profile.index',
    'permissions.profile.edit',

    'permissions.clients.index',
    'permissions.clients.edit',
    'permissions.clients.card-activation',

    'permissions.files.upload',
    'permissions.files.edit',

    'permissions.subjects.index',

    'permissions.links.index',

    'permissions.product_categories.index',
    'permissions.product_categories.edit',

    'permissions.search.index',
]

ADMIN_GROUP_RIGHTS = {}
