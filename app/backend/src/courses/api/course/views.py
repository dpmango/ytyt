from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.api.course.serializers import (
    DefaultCourseSerializers,
    DetailCourseSerializers,
)
from courses.models import Course
from courses_access.models import CourseAccess


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

    @action(methods=['POST'], detail=True, url_path='trial-access')
    def set_trial_access(self, request, pk=None, *args, **kwargs):
        """
        Предоставление доступа к бесплатному фрагменту курса
        """
        course = self.get_object()
        CourseAccess.objects.set_trial(course, user=self.request.user)

        serializers = DetailCourseSerializers(course, context=self.get_serializer_context())
        return Response(serializers.data, status=status.HTTP_201_CREATED)
