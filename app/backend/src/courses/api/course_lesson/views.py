from rest_framework import viewsets
from rest_framework.permissions import AllowAny


# from api.permission_classes import ActionBasedPermission
from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.models import CourseLesson
from courses.api.course_lesson.serializers import DefaultCourseLessonSerializers, DetailCourseLessonSerializers


class CourseLessonViewSet(FlexibleSerializerModelViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = CourseLesson.objects.all()
    permission_classes = (AllowAny, )

    action_permissions = {  # TODO: настроить права
        'list': 'courses.view_course'
    }

    serializers = {
        'default': DefaultCourseLessonSerializers,
        'retrieve': DetailCourseLessonSerializers,
    }
