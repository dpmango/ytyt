from django.db.models import Q
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING, TYPE_INTEGER
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.models import LessonFragment
from courses_access.models import Access
from search.api.serializers import DefaultCourseSearchSerializers


class SearchViewSet(FlexibleSerializerModelViewSetMixin,
                    viewsets.mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, )
    serializers = {
        'default': DefaultCourseSearchSerializers
    }

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }

    @swagger_auto_schema(
        manual_parameters=[
            Parameter('text', IN_QUERY, type=TYPE_STRING),
            Parameter('limit', IN_QUERY, type=TYPE_INTEGER),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Поиск по фрагментам урока
        Условия:
            — Поиск производится только по доступным фрагментам
            — Выводится только 5 записей (Дефолтное значение)
        """
        access = Access.objects.filter(user=self.request.user).first()

        if not access:
            return Response(
                {'detail': 'Нет доступов к курсу. Отсутствует access-модель'}, status=status.HTTP_400_BAD_REQUEST
            )

        limit = request.query_params.get('limit') or 5
        query_text = request.query_params.get('text', '')

        if len(query_text) == 0:
            return Response([], status=status.HTTP_200_OK)

        query_text = query_text.split()
        query = Q()
        for text in query_text:
            query |= Q(content__icontains=text) | Q(title__icontains=text)
            query |= Q(course_lesson__title__icontains=text) | Q(course_lesson__description__icontains=text)
            query |= Q(course_lesson__course_theme__title__icontains=text)

        # Если юзер не относится к стаф-группе, то дополняем доступными фрагментами
        if not request.user.in_stuff_groups:
            manual_accessible_fragments = access.get_objects(to_struct='lesson_fragment')
            manual_accessible_fragments = {
                item.pk for item in manual_accessible_fragments
                if access.check_manual_access('lesson_fragment', item.pk)
            }

            accessible_fragments = access.get_accessible_objects(to_struct='lesson_fragment')
            accessible_fragments = {item.pk for item in accessible_fragments}

            # Объединяем доступные фрагменты вместе с фрагментами, к которым есть ручной доступ
            accessible_fragments |= manual_accessible_fragments

            query &= Q(id__in=accessible_fragments)

        queryset = LessonFragment.objects.filter(query)
        queryset = queryset.distinct('course_lesson_id').order_by('course_lesson_id')
        queryset = queryset.select_related(
            'course_lesson', 'course_lesson__course_theme', 'course_lesson__course_theme__course'
        )
        return Response(self.get_serializer(queryset[:limit], many=True).data, status=status.HTTP_200_OK)
