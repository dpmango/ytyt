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
