from rest_framework import viewsets

from api.mixins import (
    FlexibleSerializerModelViewSetMixin, ParamsAutoFilterModelViewSetMixin
)
from courses.api.course_lesson.serializers import (
    DefaultCourseLessonSerializers, DetailCourseLessonSerializers
)
from courses.models import CourseLesson
from courses_access.permissions import CourseLessonAccessPermissions


class CourseLessonViewSet(FlexibleSerializerModelViewSetMixin,
                          ParamsAutoFilterModelViewSetMixin,
                          viewsets.ReadOnlyModelViewSet):
    lookup_mapping = {
        'course_id': 'course_theme__course_id', 'course_theme_id': 'course_theme_id', 'pk': 'pk'
    }

    queryset = CourseLesson.objects.all()
    permission_classes = (CourseLessonAccessPermissions, )

    serializers = {
        'default': DefaultCourseLessonSerializers,
        'retrieve': DetailCourseLessonSerializers,
    }

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
