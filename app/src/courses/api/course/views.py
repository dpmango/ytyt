from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.api.course.serializers import DefaultCourseSerializers
from courses.models import Course


class CourseViewSet(FlexibleSerializerModelViewSetMixin,
                    viewsets.ReadOnlyModelViewSet):

    queryset = Course.objects.all()
    permission_classes = (AllowAny, )

    serializers = {
        'default': DefaultCourseSerializers
    }
