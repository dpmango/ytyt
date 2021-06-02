from rest_framework import viewsets

from api.mixins import (
    FlexibleSerializerModelViewSetMixin,
    ParamsAutoFilterModelViewSetMixin,
    PermissionsByActionModelViewSetMixin,
)
from courses.api.course_lesson.serializers import (
    DefaultCourseLessonSerializers, DetailCourseLessonSerializers
)
from courses.models import CourseLesson
from courses_access.permissions import (
    CourseLessonAccessPermissions,
    CourseThemeAccessPermissions,
    IsInStuffGroups,
)


class CourseLessonViewSet(FlexibleSerializerModelViewSetMixin,
                          PermissionsByActionModelViewSetMixin,
                          ParamsAutoFilterModelViewSetMixin,
                          viewsets.ReadOnlyModelViewSet):
    lookup_mapping = {
        'course_id': 'course_theme__course_id', 'course_theme_id': 'course_theme_id', 'pk': 'pk'
    }

    queryset = CourseLesson.objects.all()
    permission_classes = (IsInStuffGroups | CourseLessonAccessPermissions, )
    permission_classes_by_action = {
        'list': (IsInStuffGroups | CourseThemeAccessPermissions, ),
        'retrieve': (IsInStuffGroups | CourseLessonAccessPermissions, )
    }

    serializers = {
        'default': DefaultCourseLessonSerializers,
        'retrieve': DetailCourseLessonSerializers,
    }

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
