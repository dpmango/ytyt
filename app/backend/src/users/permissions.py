GROUP_STUDENT = 1
GROUP_MENTOR = 2
GROUP_EDUCATOR = 3
GROUP_ADMINISTRATOR = 4


GROUPS = (
    (GROUP_STUDENT, 'Студент'),
    (GROUP_MENTOR, 'Наставник'),
    (GROUP_EDUCATOR, 'Педагог'),
    (GROUP_ADMINISTRATOR, 'Администратор'),
)

GROUP_COMMON_RIGHTS = [

]

GROUP_STUDENT_RIGHTS = [
    *GROUP_COMMON_RIGHTS,
    'courses.view_coursetheme',
    'courses.view_lessonfragment',
    'courses.view_courselesson',
    'courses.view_course',
]

GROUP_MENTOR_RIGHTS = [
    *GROUP_STUDENT_RIGHTS,
]

GROUP_EDUCATOR_RIGHTS = [
    *GROUP_STUDENT_RIGHTS,
]

GROUP_ADMINISTRATOR_RIGHTS = [
    *GROUP_MENTOR_RIGHTS,
    'auth.add_permission',
    'auth.change_permission',
    'auth.delete_permission',
    'auth.view_permission',
    'auth.add_group',
    'auth.change_group',
    'auth.delete_group',
    'auth.view_group',
    'users.add_user',
    'users.change_user',
    'users.delete_user',
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
    GROUP_ADMINISTRATOR: GROUP_ADMINISTRATOR_RIGHTS,
}
