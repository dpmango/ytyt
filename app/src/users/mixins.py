from django.db import models
from django.utils.translation import gettext_lazy as _
from courses.models import Course, CourseBlock, CourseBlockLesson


class AccessBase(models.Model):

    STATUS_BLOCKED = 1
    STATUS_OPEN = 2
    STATUS_IN_PROGRESS = 3
    STATUS_COMPLETED = 4
    STATUSES = (
        (STATUS_BLOCKED, 'Заблокирован'),
        (STATUS_OPEN, 'Доступен'),
        (STATUS_IN_PROGRESS, 'В процессе'),
        (STATUS_COMPLETED, 'Завершен'),
    )

    status = models.PositiveSmallIntegerField('Статус', choices=STATUSES)
    progress = models.DecimalField('Прогресс', max_digits=3, decimal_places=2, default='0.00')

    class Meta:
        abstract = True


class CourseAccess(AccessBase):
    model = models.ForeignKey(Course, on_delete=models.CASCADE)


class CourseBlockAccess(AccessBase):
    model = models.ForeignKey(CourseBlock, on_delete=models.CASCADE)


class CourseBlockLessonAccess(AccessBase):
    model = models.ForeignKey(CourseBlockLesson, on_delete=models.CASCADE)


class CoursesAccessMixin(models.Model):

    user_access_course = models.ManyToManyField(
        CourseAccess,
        verbose_name=_('Доступные курсы для пользователя'),
        blank=True,
        related_name="user_access_course_set",
        related_query_name="user_access_course",
    )

    user_access_course_block = models.ManyToManyField(
        CourseBlockAccess,
        verbose_name=_('Доступные блоки уроков для пользователя'),
        blank=True,
        related_name="user_access_course_block_set",
        related_query_name="user_access_course_block",
    )

    user_access_course_block_lesson = models.ManyToManyField(
        CourseBlockLessonAccess,
        verbose_name=_('Доступные уроки для пользователя'),
        blank=True,
        related_name="user_access_course_block_lesson_set",
        related_query_name="user_access_course_block_lesson",
    )

    class Meta:
        abstract = True
