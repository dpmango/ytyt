from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.mixins import (
    FlexibleSerializerModelViewSetMixin, ParamsAutoFilterModelViewSetMixin
)
from courses.api.course_theme.serializers import DefaultCourseThemeSerializers
from courses.models import CourseTheme


class CourseThemeViewSet(FlexibleSerializerModelViewSetMixin,
                         ParamsAutoFilterModelViewSetMixin,
                         viewsets.ReadOnlyModelViewSet):

    queryset = CourseTheme.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )

    lookup_mapping = {'course_id': 'course_id', 'pk': 'pk'}

    serializers = {
        'default': DefaultCourseThemeSerializers
    }

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
