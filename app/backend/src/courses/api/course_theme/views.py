from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.mixins import (
    FlexibleSerializerModelViewSetMixin,
    PermissionsByActionModelViewSetMixin,
    ParamsAutoFilterModelViewSetMixin,
)
from courses.api.course_theme.serializers import CourseThemeWithStatsSerializers
from courses.models import CourseTheme


class CourseThemeViewSet(FlexibleSerializerModelViewSetMixin,
                         PermissionsByActionModelViewSetMixin,
                         ParamsAutoFilterModelViewSetMixin,
                         viewsets.mixins.ListModelMixin,
                         viewsets.GenericViewSet):

    queryset = CourseTheme.objects.all()
    permission_classes = (IsAuthenticated, )
    permission_classes_by_action = {
        'list': (IsAuthenticated, ),
    }
    lookup_mapping = {'course_id': 'course_id', 'pk': 'pk'}
    serializers = {
        'default': CourseThemeWithStatsSerializers
    }

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
