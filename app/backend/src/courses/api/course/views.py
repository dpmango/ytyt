from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.api.course.serializers import (
    DefaultCourseSerializers,
    DetailCourseSerializers,
)
from courses.models import Course


class CourseViewSet(FlexibleSerializerModelViewSetMixin,
                    viewsets.ReadOnlyModelViewSet):

    queryset = Course.objects.all()
    permission_classes = (AllowAny, )

    serializers = {
        'default': DefaultCourseSerializers,
        'retrieve': DetailCourseSerializers,
    }

    def get_serializer_context(self):
        from courses_access.models import Access
        from pprint import pprint

        access = Access.objects.get(pk=1)
        access.set_empty_accesses()
        access.set_trial()

        pprint(access.course_theme)
        print()

        pprint(access.course_lesson)
        print()

        pprint(access.lesson_fragment)



        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
