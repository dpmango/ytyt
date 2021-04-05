from django.db import models
from users.models import User
from courses.models import Course, CourseTheme, CourseLesson, LessonFragment


class AccessBaseManager(models.Manager):
    def get_status(self, model, user: User) -> int:
        try:
            return self.get(user=user).status
        except (User.DoesNotExist, IndexError):
            return AccessBase.COURSES_STATUS_BLOCK


class AccessBase(models.Model):

    COURSES_STATUS_AVAILABLE = 1
    COURSES_STATUS_IN_PROGRESS = 2
    COURSES_STATUS_COMPLETED = 3
    COURSES_STATUS_BLOCK = 4

    COURSES_STATUSES = (
        (COURSES_STATUS_AVAILABLE, 'Доступен'),
        (COURSES_STATUS_IN_PROGRESS, 'В процессе'),
        (COURSES_STATUS_COMPLETED, 'Завершен'),
        (COURSES_STATUS_BLOCK, 'Заблокирован'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField('Статус', choices=COURSES_STATUSES, default=COURSES_STATUS_BLOCK)
    date_created = models.DateTimeField('Дата создаения фрагмента', auto_now=True)

    class Meta:
        abstract = True


class CourseAccessManager(models.Manager):
    def get_status(self, model, user: User) -> int:
        try:
            return self.get(user=user).status
        except (User.DoesNotExist, IndexError):
            return AccessBase.COURSES_STATUS_BLOCK


class CourseAccess(AccessBase):
    COURSE_ACCESS_TYPE_TRIAL = 1
    COURSE_ACCESS_TYPE_FULL_PAID = 2  # TODO: При сохранении из админки не давать доступ к добавлению этого параметра
    COURSE_ACCESS_TYPE_FULL_UNPAID = 3

    COURSE_ACCESS_TYPES = (
        (COURSE_ACCESS_TYPE_TRIAL, 'Пробный'),
        (COURSE_ACCESS_TYPE_FULL_PAID, 'Полный оплаченный'),
        (COURSE_ACCESS_TYPE_FULL_UNPAID, 'Полный неоплаченный'),
    )

    access_type = models.PositiveSmallIntegerField(
        'Тип статуса', choices=COURSE_ACCESS_TYPES, default=COURSE_ACCESS_TYPE_TRIAL
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    objects = CourseAccessManager()

    class Meta(AccessBase.Meta):
        abstract = False
        verbose_name = 'Доступ к курсу'
        verbose_name_plural = 'Доступ к курсам'


class CourseThemeAccess(AccessBase):
    course_theme = models.ForeignKey(CourseTheme, on_delete=models.CASCADE)

    class Meta(AccessBase.Meta):
        abstract = False
        verbose_name = 'Доступ к теме курса'
        verbose_name_plural = 'Доступ к темам курса'


class CourseLessonAccess(AccessBase):
    course_lesson = models.ForeignKey(CourseLesson, on_delete=models.CASCADE)

    class Meta(AccessBase.Meta):
        abstract = False
        verbose_name = 'Доступ к уроку'
        verbose_name_plural = 'Доступ к урокам'


class LessonFragmentAccess(AccessBase):
    lesson_fragment = models.ForeignKey(LessonFragment, on_delete=models.CASCADE)

    class Meta(AccessBase.Meta):
        abstract = False
        verbose_name = 'Доступ к фрагменту урока'
        verbose_name_plural = 'Доступ к фрагментам урока'
