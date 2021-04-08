from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.mixins import (
    FlexibleSerializerModelViewSetMixin, ParamsAutoFilterModelViewSetMixin
)
from courses.api.course_lesson.serializers import (
    DefaultCourseLessonSerializers, DetailCourseLessonSerializers
)
from courses.models import CourseLesson, CourseTheme
from courses_access.common.models import AccessBase
from courses_access.models import CourseLessonAccess


class CourseLessonViewSet(FlexibleSerializerModelViewSetMixin,
                          ParamsAutoFilterModelViewSetMixin,
                          viewsets.ReadOnlyModelViewSet):
    lookup_mapping = {
        'course_id': 'course_theme__course_id', 'course_theme_id': 'course_theme_id', 'pk': 'pk'
    }

    queryset = CourseLesson.objects.all()

    serializers = {
        'default': DefaultCourseLessonSerializers,
        'retrieve': DetailCourseLessonSerializers,
    }

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }

    @action(methods=['POST'], detail=True, url_path='request-access')
    def request_access(self, request, pk=None, *args, **kwargs):
        """
        Метод запрашивает доступ к уроку
        Дать доступ к уроку можно при выполнении одного из условий:
            - Предыдущий урок закрыт
            - Предыдущий урок не существует
        """
        course_lesson: CourseLesson = self.get_object()
        course_theme: CourseTheme = course_lesson.course_theme

        lessons = course_theme.courselesson_set.filter(order__lt=course_lesson.order)
        if len(lessons) == 0:
            CourseLessonAccess.objects.set_access_with_fragment(course_lesson, user=request.user)

        else:
            previous_lesson = max(lessons, key=lambda theme: theme.order)
            previous_lesson_access = CourseLessonAccess.objects.filter(
                course_lesson=previous_lesson, user=request.user, status=AccessBase.COURSES_STATUS_COMPLETED
            ).first()

            if previous_lesson_access is None:
                msg = 'Для доступа к уроку `%s` необходимо пройти урок `%s`' % (
                    course_lesson.title, previous_lesson.title
                )
                return Response({'detail': msg}, status=status.HTTP_400_BAD_REQUEST)

            CourseLessonAccess.objects.set_access_with_fragment(course_lesson, user=request.user)

        serializer = DefaultCourseLessonSerializers(course_lesson, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
