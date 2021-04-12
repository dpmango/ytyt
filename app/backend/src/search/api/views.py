from django.db.models import Q
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.models import LessonFragment
from search.api.serializers import DefaultCourseSearchSerializers


class SearchViewSet(FlexibleSerializerModelViewSetMixin,
                    viewsets.mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializers = {
        'default': DefaultCourseSearchSerializers
    }

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }

    @swagger_auto_schema(manual_parameters=[Parameter('text', IN_QUERY, type=TYPE_STRING)])
    def list(self, request, *args, **kwargs):
        """
        Поиск по фрагментам урока
        """

        serializer = self.get_serializer_class()
        context = self.get_serializer_context()

        query_text = request.query_params.get('text', '')
        if len(query_text) == 0:
            return Response([], status=status.HTTP_200_OK)

        query_text = query_text.split()
        query = Q()

        for text in query_text:
            query |= Q(content__icontains=text) | Q(title__icontains=text)

        queryset = LessonFragment.objects.filter(query)
        queryset = queryset.select_related('course_lesson', 'course_lesson__course_theme')
        queryset = queryset.distinct('course_lesson_id').order_by('course_lesson_id')

        return Response(serializer(queryset, many=True, context=context).data, status=status.HTTP_200_OK)
