from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.mixins import (
    FlexibleSerializerModelViewSetMixin, ParamsAutoFilterModelViewSetMixin
)
from courses.api.course_theme.serializers import DefaultCourseThemeSerializers
from courses.models import CourseTheme, Course
from courses_access.common.models import AccessBase
from courses_access.models import CourseThemeAccess


class CourseThemeViewSet(FlexibleSerializerModelViewSetMixin,
                         ParamsAutoFilterModelViewSetMixin,
                         viewsets.ReadOnlyModelViewSet):

    queryset = CourseTheme.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )

    lookup_mapping = {'course_id': 'course_id', 'pk': 'pk'}

    serializers = {
        'default': DefaultCourseThemeSerializers
    }

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }

    @action(methods=['POST'], detail=True, url_path='request-access')
    def request_access(self, request, pk=None, *args, **kwargs):
        """
        Метод запрашивает доступ к теме курса
        Дать доступ к курсу можно при выполнении одного из условий:
            - Предыдущая тема курса закрыта
            - Предыдущей темы курса не существует
        """
        course_theme: CourseTheme = self.get_object()
        course: Course = course_theme.course

        themes = course.coursetheme_set.filter(order__lt=course_theme.order)
        if len(themes) == 0:
            CourseThemeAccess.objects.set_access(
                status=AccessBase.COURSES_STATUS_IN_PROGRESS, course_theme=course_theme, user=request.user
            )

        else:
            previous_theme = max(themes, key=lambda theme: theme.order)
            previous_theme_access = CourseThemeAccess.objects.filter(
                course_theme=previous_theme, user=request.user, status=AccessBase.COURSES_STATUS_COMPLETED
            ).first()

            if previous_theme_access is None:
                msg = 'Для доступа к теме `%s` необхожимо пройти тему `%s`' % (course_theme.title, previous_theme.title)
                return Response({'detail': msg}, status=status.HTTP_400_BAD_REQUEST)

            CourseThemeAccess.objects.set_access(
                status=AccessBase.COURSES_STATUS_IN_PROGRESS, course_theme=course_theme, user=request.user
            )

        serializer = DefaultCourseThemeSerializers(course_theme, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
