from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.permission_classes import ActionBasedPermission
from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.api.course_theme.serializers import DefaultCourseThemeSerializers
from courses.models import LessonFragment


class LessonFragmentViewSet(FlexibleSerializerModelViewSetMixin,
                            viewsets.GenericViewSet):

    permission_classes = (AllowAny, )
    # action_permissions = {  # TODO: настроить права
    #     'ping': 'courses.view_course'
    # }

    @action(methods=['POST'], detail=True)
    def check(self, request, pk=None, *args, **kwargs):

        user = request.user

        last_fragment = user.user_access_course_lesson.all()
        print(last_fragment)




        return Response(status=status.HTTP_204_NO_CONTENT)
