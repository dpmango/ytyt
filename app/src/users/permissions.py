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
– permissions.users.index – просматривать пользователей
– permissions.users.edit – редактировать пользователей

"""

GROUP_RIGHTS[GROUP_ADMINISTRATOR] = [
    'permissions.admin.index',
    'permissions.admin.@superuser',

    'permissions.users.index',
    'permissions.users.edit',
]

GROUP_RIGHTS[GROUP_REVIEWER] = [

]

ADMIN_GROUP_RIGHTS = {}


from rest_framework.permissions import AllowAny


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True

        for action, permission_name in getattr(view, 'action_permissions', {}).items():
            if view.action == action:
                if request.user is None or not request.user.is_authenticated:
                    return False
                if request.user.has_perm(permission_name):
                    return True
        return False
