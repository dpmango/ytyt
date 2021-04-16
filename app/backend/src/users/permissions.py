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


#  admin.add_logentry
#  admin.change_logentry
#  admin.delete_logentry
#  admin.view_logentry
#  auth.add_permission
#  auth.change_permission
#  auth.delete_permission
#  auth.view_permission
#  auth.add_group
#  auth.change_group
#  auth.delete_group
#  auth.view_group
#  contenttypes.add_contenttype
#  contenttypes.change_contenttype
#  contenttypes.delete_contenttype
#  contenttypes.view_contenttype
#  sessions.add_session
#  sessions.change_session
#  sessions.delete_session
#  sessions.view_session
#  sites.add_site
#  sites.change_site
#  sites.delete_site
#  sites.view_site
#  authtoken.add_token
#  authtoken.change_token
#  authtoken.delete_token
#  authtoken.view_token
#  authtoken.add_tokenproxy
#  authtoken.change_tokenproxy
#  authtoken.delete_tokenproxy
#  authtoken.view_tokenproxy
#  account.add_emailaddress
#  account.change_emailaddress
#  account.delete_emailaddress
#  account.view_emailaddress
#  account.add_emailconfirmation
#  account.change_emailconfirmation
#  account.delete_emailconfirmation
#  account.view_emailconfirmation
#  socialaccount.add_socialaccount
#  socialaccount.change_socialaccount
#  socialaccount.delete_socialaccount
#  socialaccount.view_socialaccount
#  socialaccount.add_socialapp
#  socialaccount.change_socialapp
#  socialaccount.delete_socialapp
#  socialaccount.view_socialapp
#  socialaccount.add_socialtoken
#  socialaccount.change_socialtoken
#  socialaccount.delete_socialtoken
#  socialaccount.view_socialtoken
#  users.add_coursethemeaccess
#  users.change_coursethemeaccess
#  users.delete_coursethemeaccess
#  users.view_coursethemeaccess
#  users.add_courselessonaccess
#  users.change_courselessonaccess
#  users.delete_courselessonaccess
#  users.view_courselessonaccess
#  users.add_courseaccess
#  users.change_courseaccess
#  users.delete_courseaccess
#  users.view_courseaccess
#  users.add_user
#  users.change_user
#  users.delete_user
#  users.view_user
#  courses.add_course
#  courses.change_course
#  courses.delete_course
#  courses.view_course
#  courses.add_courselesson
#  courses.change_courselesson
#  courses.delete_courselesson
#  courses.view_courselesson
#  courses.add_lessonfragment
#  courses.change_lessonfragment
#  courses.delete_lessonfragment
#  courses.view_lessonfragment
#  courses.add_coursetheme
#  courses.change_coursetheme
#  courses.delete_coursetheme
#  courses.view_coursetheme

