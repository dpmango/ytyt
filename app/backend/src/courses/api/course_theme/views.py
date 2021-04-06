from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly


from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.models import CourseTheme
from courses.api.course_theme.serializers import DefaultCourseThemeSerializers


class CourseThemeViewSet(FlexibleSerializerModelViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = CourseTheme.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )

    action_permissions = {  # TODO: настроить права
        'list': 'courses.view_course'
    }

    serializers = {
        'default': DefaultCourseThemeSerializers
    }

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
