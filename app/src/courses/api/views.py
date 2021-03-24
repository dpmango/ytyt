from rest_framework import viewsets, status
from rest_framework.response import Response

from api.permission_classes import ActionBasedPermission


class CoursesViewSet(viewsets.ViewSet):
    permission_classes = (ActionBasedPermission, )

    action_permissions = {
        'list': 'courses.view_course'
    }

    def list(self, request):
        return Response({'test': 'ok'}, status=status.HTTP_200_OK)
