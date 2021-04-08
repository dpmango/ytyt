from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.api.lesson_fragment.serializers import DefaultLessonFragmentSerializers
from courses.models import LessonFragment, CourseLesson, CourseTheme
from courses_access.common.models import AccessBase
from courses_access.models import LessonFragmentAccess, CourseThemeAccess, CourseLessonAccess, CourseAccess


class LessonFragmentViewSet(FlexibleSerializerModelViewSetMixin,
                            viewsets.GenericViewSet):

    queryset = LessonFragment.objects.all()
    permission_classes = (IsAuthenticated, )
    serializers = {
        'default': DefaultLessonFragmentSerializers
    }

    @action(methods=['POST'], detail=True, url_path='completed')
    def set_completed(self, request, pk=None, *args, **kwargs):
        """
        Логика закрытия выбранного фрагмента урока:
        - Не завершающий фрагмент в уроке:
            1. Фрагмент закрывается со статусом `Завершен`
            2. Предоставляется доступ к следующему фрагменту урока

        - Завершающий фрагмент в уроке:
            1. Фрагмент урока закрывается
            2. Урок закрывается со статусом `Завершен`

        - Завершающий фрагмент в последнем уроке темы:
            1. Фрагмент урока закрывается
            2. Урок закрывается со статусом `Завершен`
            3. Тема закрывается со статусом `Завершен`

        - Последний фрагмент в последнем уроке завершающей темы курса:
            1. Фрагмент урока закрывается
            2. Урок закрывается со статусом `Завершен`
            3. Тема закрывается со статусом `Завершен`
            4. Курс закрывается со статусом `Завершен` (фанфары)
        """
        lesson_fragment: LessonFragment = self.get_object()
        serializer = self.get_serializer_class()
        context = self.get_serializer_context()

        with transaction.atomic():
            course_lesson = lesson_fragment.course_lesson
            course_theme = course_lesson.course_theme
            course = course_theme.course
            user = request.user

            # Закрываем текущий фрагмент урока
            LessonFragmentAccess.objects.set_status(lesson_fragment, user, AccessBase.COURSES_STATUS_COMPLETED)

            lesson_fragments = course_lesson.lessonfragment_set.filter(pk__gt=lesson_fragment.id)
            lesson_fragment = lesson_fragments.first()

            # Предоставляем доступ к следующему фрагменту если существуют доступные фрагменты
            if lesson_fragment:
                LessonFragmentAccess.objects.set_access(
                    lesson_fragment=lesson_fragment, user=user, status=AccessBase.COURSES_STATUS_AVAILABLE
                )
                return Response(serializer(lesson_fragment, context=context), status=status.HTTP_202_ACCEPTED)

            # Если доступных фрагментов в уроке нет, то необходимо закрыть урок
            CourseLessonAccess.objects.set_status(course_lesson, user, AccessBase.COURSES_STATUS_COMPLETED)

            # TODO: переделать на один sql-запрос а-ка exists()
            count_lessons = CourseLesson.objects.filter(course_theme=course_theme).count()
            count_lessons_completed = CourseLessonAccess.objects.filter(
                user=user, status=AccessBase.COURSES_STATUS_COMPLETED
            ).count()

            # Если количество пройденных уроков совпадает, то нужно закрывать текущую тему
            if count_lessons == count_lessons_completed:
                CourseThemeAccess.objects.set_status(course_theme, user, AccessBase.COURSES_STATUS_COMPLETED)

                count_themes = CourseTheme.objects.filter(course=course).count()
                count_themes_completed = CourseThemeAccess.objects.filter(
                    user=user, status=AccessBase.COURSES_STATUS_COMPLETED
                ).count()

                # Если количество пройденных тем совпадает с общим количеством, то необходимо закрыть курс
                if count_themes == count_themes_completed:
                    CourseAccess.objects.set_status(course, user, AccessBase.COURSES_STATUS_COMPLETED)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
