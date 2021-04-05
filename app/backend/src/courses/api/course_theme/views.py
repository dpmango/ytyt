from rest_framework import viewsets
from rest_framework.permissions import AllowAny


# from api.permission_classes import ActionBasedPermission
from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.models import CourseTheme
from courses.api.course_theme.serializers import DefaultCourseThemeSerializers


class CourseThemeViewSet(FlexibleSerializerModelViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = CourseTheme.objects.all()
    permission_classes = (AllowAny, )

    action_permissions = {  # TODO: настроить права
        'list': 'courses.view_course'
    }

    serializers = {
        'default': DefaultCourseThemeSerializers
    }
