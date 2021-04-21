from django.db import transaction
from rest_framework import exceptions
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.mixins import FlexibleSerializerModelViewSetMixin
from courses.api.lesson_fragment.serializers import DetailLessonFragmentSerializers
from courses.models import LessonFragment
from courses_access.common.models import AccessBase
from courses_access.models import LessonFragmentAccess, CourseThemeAccess, CourseLessonAccess, CourseAccess
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
            user = request.user

            # Закрываем текущий фрагмент урока
            LessonFragmentAccess.objects.set_status(lesson_fragment, user, AccessBase.COURSES_STATUS_COMPLETED)

            # Получаем следующий доступный фрагмент урока
            next_lesson_fragment = course_lesson.lessonfragment_set.filter(pk__gt=lesson_fragment.id).first()

            # Если существует следующий фрагмент, то предоставляем доступ к нему
            if next_lesson_fragment is not None:
                next_lesson_fragment_status = LessonFragmentAccess.objects.get_status(next_lesson_fragment, user)

                # Для экономии запросов — проверяем факт выдачи доступа ранее
                if next_lesson_fragment_status not in AccessBase.AVAILABLE_STATUSES:
                    LessonFragmentAccess.objects.set_access(
                        lesson_fragment=next_lesson_fragment, user=user, status=AccessBase.COURSES_STATUS_AVAILABLE
                    )

                return Response(serializer(next_lesson_fragment, context=context).data, status=status.HTTP_202_ACCEPTED)

            # Если следующего фрагмента урока не существует
            # Берем информацию о теме курса и о самом курсе
            course_theme = course_lesson.course_theme
            course = course_theme.course

            # Закрываем текущий урок
            CourseLessonAccess.objects.set_status(course_lesson, user, AccessBase.COURSES_STATUS_COMPLETED)

            # Выбираем следующий урок
            next_course_lesson = course_theme.courselesson_set.filter(order__gt=course_lesson.order).first()

            # Если следующий урок существует, то к нему и первому фрагменту необходимо предоставить доступы
            if next_course_lesson is not None:
                CourseLessonAccess.objects.set_access_with_fragment(next_course_lesson, user)

                data = {'course_id': course.id, 'course_theme_id': course_theme.id}
                return Response(data, status=status.HTTP_202_ACCEPTED)

            # Если следующего урока не существует
            # Закрываем текущую тему курса
            CourseThemeAccess.objects.set_status(course_theme, user, AccessBase.COURSES_STATUS_COMPLETED)

            # Берем информацию по доступу к курсу
            course_access = CourseAccess.objects.filter(course=course, user=user).first()

            # Выбираем мледующую доступную тему
            next_course_theme = course.coursetheme_set.filter(order__gt=course_theme.order).first()
            if next_course_theme is not None:

                # Если следующая тема НЕ бесплатная и у пользователя НЕ оплачен курс, то вернем ему ошибку доступа
                # В противном случае — даем доступ к следующей теме
                if not next_course_theme.free_access and \
                        course_access.access_type not in AccessBase.AVAILABLE_ACCESS_TYPES_FULL:
                    msg = 'Для доступа к теме `%s` вам необходимо произвести оплату' % next_course_theme.title
                    return Response({'detail': msg}, status=status.HTTP_403_FORBIDDEN)

                # Проверка на скорость прохождения курса
                CourseThemeAccess.objects.check_learning_speed(request.user, course_access)

                CourseThemeAccess.objects.set_access_with_lesson(next_course_theme, user)
                return Response({'course_id': course.id}, status=status.HTTP_202_ACCEPTED)

            CourseAccess.objects.set_status(course, user, AccessBase.COURSES_STATUS_COMPLETED)
        # Если доступной темы нет, то курс закончен
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
