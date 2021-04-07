from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.api.lesson_fragment.serializers import DefaultLessonFragmentSerializers
from courses.models import LessonFragment
from courses_access.common.models import AccessBase
from courses_access.models import LessonFragmentAccess, CourseThemeAccess, CourseLessonAccess
from courses_access.permissions import LessonFragmentAccessPermissions


class LessonFragmentViewSet(FlexibleSerializerModelViewSetMixin,
                            viewsets.GenericViewSet):

    queryset = LessonFragment.objects.all()
    permission_classes = (IsAuthenticated, LessonFragmentAccessPermissions)
    serializers = {
        'set_completed': DefaultLessonFragmentSerializers
    }

    @action(methods=['POST'], detail=True, url_path='completed')
    def set_completed(self, request, pk=None, *args, **kwargs):
        """
        Метод завершает выбранный фрагмент урока
        """
        # TODO: сначала написать общий алгоритм, потом учесть, что могут быть бесплатные курсы
        # TODO: при бесплатных курсах дальше бесплатных тем уходить нельзя
        # TODO: для этого тип доступа к курсу должен быть НЕ триал

        lesson_fragment: LessonFragment = self.get_object()
        serializer = self.get_serializer_class()
        context = self.get_serializer_context()

        with transaction.atomic():
            course_lesson = lesson_fragment.course_lesson
            course_theme = course_lesson.course_theme
            course = course_theme.course
            user = request.user

            # 1
            # Закрываем текущий фрагмент урока
            LessonFragmentAccess.objects.set_status(lesson_fragment, user, AccessBase.COURSES_STATUS_COMPLETED)

            # Выбираем следующий доступный фрагмент урока к которому мы не предоставляли доступ пользователю
            access_fragments = LessonFragmentAccess.objects.filter(
                user=user, lesson_fragment__course_lesson=course_lesson
            )
            access_fragments = access_fragments.select_related('lesson_fragment')
            access_fragments = access_fragments.values_list('lesson_fragment', flat=True)

            second_fragment = course_lesson.lessonfragment_set.filter(~Q(id__in=access_fragments))
            second_fragment = second_fragment.order_by('id').first()

            # Предоставляем доступ к следующему доступному фрагменту и возвращаем его в сериализованном виде
            if second_fragment is not None:
                LessonFragmentAccess.objects.set_access(
                    status=AccessBase.COURSES_STATUS_AVAILABLE, lesson_fragment=second_fragment, user=user
                )
                return Response(serializer(second_fragment, context=context).data, status=status.HTTP_202_ACCEPTED)

            # 2
            # Закрываем текущий урок
            CourseLessonAccess.objects.set_status(course_lesson, user, AccessBase.COURSES_STATUS_COMPLETED)

            # Выбираем следующий доступный урок из темы курса
            access_lessons = CourseLessonAccess.objects.filter(user=user, course_lesson__course_theme=course_theme)
            access_lessons = access_lessons.select_related('course_lesson').values_list('course_lesson', flat=True)

            second_lesson = course_theme.courselesson_set.filter(~Q(id__in=access_lessons)).order_by('id').first()

            # Если следующий урок существует, то необходимо предоставить к нему доступ
            if second_lesson is not None:
                CourseLessonAccess.objects.set_access(
                    status=AccessBase.COURSES_STATUS_IN_PROGRESS, course_lesson=second_lesson, user=user
                )

                # Если существует первый фрагмент урока, то нужно предоставить доступ к нему
                second_fragment = second_lesson.lessonfragment_set.order_by('id').first()

                if second_fragment is None:
                    return Response({'detail': 'У выбранного урока нет фрагментов'}, status=status.HTTP_200_OK)

                LessonFragmentAccess.objects.set_access(
                    status=AccessBase.COURSES_STATUS_AVAILABLE, lesson_fragment=second_fragment, user=user
                )

                return Response(serializer(second_fragment, context=context).data, status=status.HTTP_202_ACCEPTED)

            # 3
            # Закрываем текущую тему курса
            CourseThemeAccess.objects.set_status(course_theme, user, AccessBase.COURSES_STATUS_COMPLETED)

            access_themes = CourseThemeAccess.objects.filter(user=user, course_theme__course=course)
            access_themes = access_themes.select_related('course_theme').values_list('course_theme', flat=True)

            second_theme = course.coursetheme_set.filter(~Q(id__in=access_themes)).order_by('id').first()
            if second_theme is not None:

                CourseThemeAccess.objects.set_access(
                    status=AccessBase.COURSES_STATUS_IN_PROGRESS, course_theme=second_theme, user=user
                )

                second_lesson = second_theme.courselesson_set.order_by('id').first()
                if second_lesson is None:
                    return Response({'detail': 'У выбранного темы нет уроков'}, status=status.HTTP_200_OK)

                CourseLessonAccess.objects.set_access(
                    status=AccessBase.COURSES_STATUS_IN_PROGRESS, course_lesson=second_lesson, user=user
                )

                second_fragment = second_lesson.lessonfragment_set.order_by('id').first()
                if second_fragment is None:
                    return Response({'detail': 'У выбранного урока нет фрагментов'}, status=status.HTTP_200_OK)

                LessonFragmentAccess.objects.set_access(
                    status=AccessBase.COURSES_STATUS_AVAILABLE, lesson_fragment=second_fragment, user=user
                )

                return Response(serializer(second_fragment, context=context).data, status=status.HTTP_202_ACCEPTED)

        return Response({'detail': 'По курсу больше нет доступных тем'}, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
