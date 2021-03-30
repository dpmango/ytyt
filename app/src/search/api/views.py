from django.db.models import Q
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

    def list(self, request, *args, **kwargs):
        """
        Поиск по фрагментам урока
        """

        query_text = request.query_params.get('text', '')
        query_text = query_text.split()

        query = Q()
        for text in query_text:
            query |= Q(description__icontains=text) | Q(title__icontains=text)

        queryset = LessonFragment.objects.filter(query)
        queryset = queryset.distinct('id').select_related('course_lesson', 'course_lesson__course_theme')

        serializer = self.get_serializer_class()
        serializer = serializer(queryset, many=True, context={'query_text': query_text})

        return Response(serializer.data, status=status.HTTP_200_OK)
