from django.db import models
from django.utils.translation import gettext_lazy as _

from courses.models import Course, CourseTheme, CourseLesson


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

    updated_date = models.DateTimeField('Дата обновления', auto_now=True)
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-updated_date', '-created_date')


class CourseAccess(AccessBase):
    model = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta(AccessBase.Meta):
        abstract = False
        verbose_name = 'Доступ к курсу'
        verbose_name_plural = 'Доступ к курсам'

    def __str__(self):
        return '%s' % self.model.title


class CourseThemeAccess(AccessBase):
    model = models.ForeignKey(CourseTheme, on_delete=models.CASCADE)

    class Meta(AccessBase.Meta):
        abstract = False
        verbose_name = 'Доступ к теме курса'
        verbose_name_plural = 'Доступ к темам курса'

    def __str__(self):
        return '%s | %s' % (self.model.course.title, self.model.title)


class CourseLessonAccess(AccessBase):
    model = models.ForeignKey(CourseLesson, on_delete=models.CASCADE)
    fragments_passed = models.IntegerField('Количество пройденных фрагментов урока', default=0)

    class Meta(AccessBase.Meta):
        abstract = False
        verbose_name = 'Доступ к уроку'
        verbose_name_plural = 'Доступ к урокам'

    def __str__(self):
        return '%s | %s | %s' % (
            self.model.course_theme.course.title, self.model.course_theme.title, self.model.title
        )


class CoursesAccessMixin(models.Model):
    """
    Миксин-класс для расширения модели пользователя информацией по курсам
    """

    user_access_course = models.ManyToManyField(
        CourseAccess,
        verbose_name=_('Доступные курсы для пользователя'),
        blank=True,
        related_name="user_access_course_set",
        related_query_name="user_access_course",
    )

    user_access_course_theme = models.ManyToManyField(
        CourseThemeAccess,
        verbose_name=_('Доступные блоки уроков для пользователя'),
        blank=True,
        related_name="user_access_course_theme_set",
        related_query_name="user_access_course_theme",
    )

    user_access_course_lesson = models.ManyToManyField(
        CourseLessonAccess,
        verbose_name=_('Доступные уроки для пользователя'),
        blank=True,
        related_name="user_access_course_lesson_set",
        related_query_name="user_access_course_lesson",
    )

    class Meta:
        abstract = True
