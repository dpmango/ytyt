from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.permissions import ActionBasedPermission

User = get_user_model()


class CoursesViewSet(viewsets.ViewSet):

    def list(self, request):


        return Response([1, 2, 3], status=status.HTTP_200_OK)

