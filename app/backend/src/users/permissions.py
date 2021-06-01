GROUP_STUDENT = 1
GROUP_MENTOR = 2
GROUP_EDUCATOR = 3
GROUP_ADMINISTRATOR = 4
GROUP_SUPPORT = 5


GROUPS = (
    (GROUP_STUDENT, 'Студент'),
    (GROUP_MENTOR, 'Наставник'),
    (GROUP_EDUCATOR, 'Педагог'),
    (GROUP_ADMINISTRATOR, 'Администратор'),
    (GROUP_SUPPORT, 'Поддержка'),
)

GROUPS_SYNC_DEFAULTS_EMAILS = {
    GROUP_MENTOR: 'mentor@ytyt.ru',
    GROUP_EDUCATOR: 'educator@ytyt.ru',
    GROUP_SUPPORT: 'support@ytyt.ru',
}


GROUP_COMMON_RIGHTS = [

]

GROUP_STUDENT_RIGHTS = [
    *GROUP_COMMON_RIGHTS,
]

GROUP_MENTOR_RIGHTS = [
    *GROUP_STUDENT_RIGHTS,
    'courses.view_coursetheme',
    'courses.view_lessonfragment',
    'courses.view_courselesson',
    'courses.view_course',
]

GROUP_EDUCATOR_RIGHTS = [
    *GROUP_STUDENT_RIGHTS,
    'courses.view_coursetheme',
    'courses.view_lessonfragment',
    'courses.view_courselesson',
    'courses.view_course',
]

GROUP_SUPPORT_RIGHTS = [
    *GROUP_EDUCATOR_RIGHTS,
    'dialogs.view_dialog',
]

GROUP_ADMINISTRATOR_RIGHTS = [
    *GROUP_SUPPORT_RIGHTS,
    'users.add_user',
    'users.change_user',
    'users.view_user',
    'courses.add_course',
    'courses.change_course',
    'courses.delete_course',
    'courses.view_course',
    'courses.add_courselesson',
    'courses.change_courselesson',
    'courses.delete_courselesson',
    'courses.view_courselesson',
    'courses.add_lessonfragment',
    'courses.change_lessonfragment',
    'courses.delete_lessonfragment',
    'courses.view_lessonfragment',
    'courses.add_coursetheme',
    'courses.change_coursetheme',
    'courses.delete_coursetheme',
    'courses.view_coursetheme',
]

GROUP_RIGHTS = {
    GROUP_STUDENT: GROUP_STUDENT_RIGHTS,
    GROUP_MENTOR: GROUP_MENTOR_RIGHTS,
    GROUP_EDUCATOR: GROUP_EDUCATOR_RIGHTS,
    GROUP_ADMINISTRATOR: GROUP_ADMINISTRATOR_RIGHTS,
    GROUP_SUPPORT: GROUP_SUPPORT_RIGHTS,
}
