from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.api.course.serializers import (
    DefaultCourseSerializers,
    DetailCourseSerializers,
)
from courses.models import Course


class CourseViewSet(FlexibleSerializerModelViewSetMixin,
                    viewsets.ReadOnlyModelViewSet):

    queryset = Course.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )

    serializers = {
        'default': DefaultCourseSerializers,
        'retrieve': DetailCourseSerializers,
    }

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
