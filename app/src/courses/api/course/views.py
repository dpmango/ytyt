from rest_framework import viewsets
from rest_framework.permissions import AllowAny


# from api.permission_classes import ActionBasedPermission
from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.models import Course
from courses.api.course.serializers import DefaultCourseSerializers


class CourseViewSet(FlexibleSerializerModelViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    permission_classes = (AllowAny, )

    action_permissions = {  # TODO: настроить права
        'list': 'courses.view_course'
    }

    serializers = {
        'default': DefaultCourseSerializers
    }

