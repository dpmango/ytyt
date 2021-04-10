from django.db import models, transaction

from courses.models import CourseLesson
from courses_access.common.models import AccessManagerBase, AccessBase
from courses_access.models.lesson_fragment import LessonFragmentAccess
from users.models import User


class CourseLessonAccessManager(AccessManagerBase):
    """
    Базовый менеджер для работы с доступами к урокам курса
    """

    def set_trial(self, course_lesson: CourseLesson, **kwargs):
        self.set_access(course_lesson=course_lesson, **kwargs)
        lesson_fragment = course_lesson.lessonfragment_set.first()

        if lesson_fragment:
            LessonFragmentAccess.objects.set_trial(lesson_fragment=lesson_fragment, **kwargs)

    def set_access_with_fragment(self, course_lesson: CourseLesson, user: User) -> None:
        """
        Метод предоставляет доступ к выбранному уроку и первому фрагменту этого урока
        :param course_lesson: Урок
        :param user: User
        """
        with transaction.atomic():
            status = AccessBase.COURSES_STATUS_AVAILABLE
            self.set_access(status=status, course_lesson=course_lesson, user=user)

            lesson_fragment = course_lesson.lessonfragment_set.order_by('id').first()
            if lesson_fragment:
                LessonFragmentAccess.objects.set_access(
                    lesson_fragment=lesson_fragment, user=user, status=status
                )

    def check_permission(self, course_lesson_id, user) -> bool:
        """
        Проверка доступа к уроку
        Обязательные условия предоставления доступа:
            1. У юзера отсутствует блокировка к курсу
            2. У юзера нет явной блокировки к выбранному уроку
        Общие условия предоставления курса:
            1. Пользователь имеет нужный доступ к уроку в связи с прохождением предыдущего урока (status)
            2. Пользователь оплатил доступ к курсу
        Примечание:
            - Если выбранная тема бесплатная, то доступ предоставляется без проверки оплаты в общем порядке
        :param course_lesson_id: ID урока
        :param user: User
        """
        course_lesson_access = self.filter(course_lesson_id=course_lesson_id, user=user)
        course_lesson_access = course_lesson_access.select_related('course_lesson').first()

        if not course_lesson_access:
            return False

        if course_lesson_access.status == AccessBase.COURSES_STATUS_BLOCK:
            return False

        course_theme = course_lesson_access.course_lesson.course_theme
        if course_theme.free_access:
            return bool(course_lesson_access.status in AccessBase.AVAILABLE_STATUSES)

        course_access = course_theme.course.courseaccess_set.filter(user=user).first()
        return bool(
            course_lesson_access.status in AccessBase.AVAILABLE_STATUSES and
            course_access.access_type in AccessBase.AVAILABLE_ACCESS_TYPES_FULL
        )


class CourseLessonAccess(AccessBase):
    course_lesson = models.ForeignKey(CourseLesson, on_delete=models.CASCADE)
    objects = CourseLessonAccessManager()

    class Meta(AccessBase.Meta):
        verbose_name = 'Доступ к уроку'
        verbose_name_plural = 'Доступ к урокам'
