from django.db import models

from courses.models import CourseLesson
from courses_access.common.models import AccessManagerBase, AccessBase
from courses_access.models.lesson_fragment import LessonFragmentAccess


class CourseLessonAccessManager(AccessManagerBase):
    """
    Базовый менеджер для работы с доступами к урокам курса
    """

    def set_trial(self, course_lesson: CourseLesson, **kwargs):
        self.set_access(course_lesson=course_lesson, **kwargs)
        lesson_fragment = course_lesson.lessonfragment_set.first()

        if lesson_fragment:
            LessonFragmentAccess.objects.set_trial(lesson_fragment=lesson_fragment, **kwargs)


class CourseLessonAccess(AccessBase):
    course_lesson = models.ForeignKey(CourseLesson, on_delete=models.CASCADE)
    objects = CourseLessonAccessManager()

    class Meta(AccessBase.Meta):
        abstract = False
        verbose_name = 'Доступ к уроку'
        verbose_name_plural = 'Доступ к урокам'
