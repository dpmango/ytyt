from django.db.models import Q
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# from api.permission_classes import ActionBasedPermission
from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.models import LessonFragment
from search.api.serializers import DefaultCourseSearchSerializers


class SearchViewSet(FlexibleSerializerModelViewSetMixin,
                    viewsets.mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    permission_classes = (AllowAny, )
    action_permissions = {  # TODO: настроить права
        'list': 'courses.view_course'
    }

    serializers = {
        'default': DefaultCourseSearchSerializers
    }

    @swagger_auto_schema(manual_parameters=[Parameter('text', IN_QUERY, type=TYPE_STRING)])
    def list(self, request, *args, **kwargs):
        """
        Поиск по фрагментам урока
        """
        query_text = request.query_params.get('text', '')
        if len(query_text) == 0:
            return Response([], status=status.HTTP_200_OK)

        query_text = query_text.split()
        query = Q()

        for text in query_text:
            query |= Q(description__icontains=text) | Q(title__icontains=text)

        queryset = LessonFragment.objects.filter(query)
        queryset = queryset.distinct('id').select_related('course_lesson', 'course_lesson__course_theme')

        serializer = self.get_serializer_class()
        return Response(serializer(queryset, many=True).data, status=status.HTTP_200_OK)
