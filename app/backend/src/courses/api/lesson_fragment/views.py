from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.api.lesson_fragment.serializers import DetailLessonFragmentSerializers
from courses.models import CourseTheme, LessonFragment
from courses_access.models import Access
from courses_access.permissions import LessonFragmentAccessPermissions


class LessonFragmentViewSet(FlexibleSerializerModelViewSetMixin,
                            viewsets.GenericViewSet):

    queryset = LessonFragment.objects.all()
    permission_classes = (LessonFragmentAccessPermissions, )
    serializers = {
        'default': DetailLessonFragmentSerializers,
    }

    @action(methods=['POST'], detail=True, url_path='completed')
    def set_completed(self, request, pk=None, *args, **kwargs):
        """
        Логика закрытия выбранного фрагмента урока:
        - Если существует следующий фрагмент в уроке:
            1. Фрагмент закрывается со статусом `Завершен`
            2. Предоставляется доступ к следующему фрагменту урока

        - Если следующего фрагмента в уроке не существует:
            1. Фрагмент урока закрывается со статусом `Завершен`
            2. Урок закрывается со статусом `Завершен`
            3. Предоставляется доступ к следующему уроку со статусом `Доступен`
            4. Предоставляется доступ к первому фрагменту нового урока со статусом `Доступен`

        - Если фрагмент завершающий для:  урока И темы:
            1. Фрагмент урока закрывается со статусом `Завершен`
            2. Урок закрывается со статусом `Завершен`
            3. Тема закрывается со статусом `Завершен`
            4. Предоставляется доступ к следующей теме со статусом `Доступен`
            5. Предоставляется доступ к первому уроку новой темы со статусом `Доступен`
            6. Предоставляется доступ к первому фрагменту нового урока со статусом `Доступен`

        - Последний фрагмент в последнем уроке завершающей темы курса:
            1. Фрагмент урока закрывается со статусом `Завершен`
            2. Урок закрывается со статусом `Завершен`
            3. Тема закрывается со статусом `Завершен`
            4. Курс закрывается со статусом `Завершен`

        Дополнительные проверки:
            1. Проверка скорости прохождения тем курса:
                Условия пропуска проверки:
                    - Пользователь является сотрудником сервиса
                    - У пользователя пройдено 0 или 1 тема
                Условия блокирования доступа к курсу:
                    - Разница между прохождением двух тем — менее одного дня
        """
        lesson_fragment: LessonFragment = self.get_object()
        context = self.get_serializer_context()
        serializer = self.get_serializer_class()

        with transaction.atomic():
            course_lesson = lesson_fragment.course_lesson
            course_theme = course_lesson.course_theme
            course = course_theme.course

            access = Access.objects.filter(user=request.user, course=course).first()

            if access.get_status('lesson_fragment', pk=pk) == Access.STATUS_COMPLETED:
                msg = 'Фрагмент `%s` уже завершен' % lesson_fragment.title
                return Response({'detail': msg}, status=status.HTTP_400_BAD_REQUEST)

            # Закрываем текущий фрагмент урока
            access.set_completed_lesson_fragment(pk=pk)

            # Получаем следующий доступный фрагмент урока
            next_lesson_fragment = access.get_next_lesson_fragment(pk=pk)

            # Если существует следующий фрагмент, то предоставляем доступ к нему
            if next_lesson_fragment is not None:
                access.set_status_lesson_fragment(pk=next_lesson_fragment.pk, status=Access.STATUS_AVAILABLE)

                next_lesson_fragment = LessonFragment.objects.get(pk=next_lesson_fragment.pk)
                context = {**context, 'set_progress': True}

                return Response(
                    serializer(next_lesson_fragment, context=context).data, status=status.HTTP_202_ACCEPTED
                )

            # Если следующего фрагмента урока не существует
            # Закрываем текущий урок
            access.set_completed_course_lesson(pk=course_lesson.pk)

            # Выбираем следующий урок
            next_course_lesson = access.get_next_course_lesson(pk=course_lesson.pk)

            # Если следующий урок существует, то к нему и первому фрагменту необходимо предоставить доступы
            if next_course_lesson is not None:
                access.set__course_lesson__lesson_fragment(pk=next_course_lesson.pk)

                data = {'course_id': course.id, 'course_theme_id': course_theme.id}
                return Response(data, status=status.HTTP_202_ACCEPTED)

            # Если следующего урока не существует
            # Закрываем текущую тему курса
            access.set_completed_course_theme(pk=course_theme.pk)

            # Выбираем следующую доступную тему
            next_course_theme = access.get_next_course_theme(pk=course_theme.pk)

            if next_course_theme is not None:

                # Если следующая тема НЕ бесплатная и у пользователя НЕ оплачен курс, то вернем ему ошибку доступа
                # В противном случае — даем доступ к следующей теме
                if not next_course_theme.free_access and \
                        access.access_type not in Access.AVAILABLE_ACCESS_TYPES_FULL:

                    next_course_theme = CourseTheme.objects.get(pk=next_course_theme.pk)
                    msg = 'Для доступа к теме `%s` вам необходимо произвести оплату' % next_course_theme.title

                    return Response({'detail': msg}, status=status.HTTP_403_FORBIDDEN)

                access.set__course_theme__course_lesson__lesson_fragment(pk=next_course_theme.pk)

                # Проверка на скорость прохождения курса
                # Делаем ее сразу после того, как предоставили доступы
                check_result = access.check_learning_speed()
                if isinstance(check_result, dict):
                    return Response(check_result, status=status.HTTP_400_BAD_REQUEST)

                return Response({'course_id': course.id}, status=status.HTTP_202_ACCEPTED)

            # Если доступной темы нет, то курс закончен.
            access.set_completed_course()

            # Дополнительно удаляем ревьюера у пользователя
            request.user.remove_reviewer()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
