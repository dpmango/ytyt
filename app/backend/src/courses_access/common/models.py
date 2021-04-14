import typing
from abc import abstractmethod

from django.db import models
from users.models import User
from django.utils import timezone


class AccessStatuses:
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

    AVAILABLE_STATUSES = (
        COURSES_STATUS_AVAILABLE,
        COURSES_STATUS_IN_PROGRESS,
        COURSES_STATUS_COMPLETED
    )

    COURSE_ACCESS_TYPE_TRIAL = 1
    COURSE_ACCESS_TYPE_FULL_PAID = 2
    COURSE_ACCESS_TYPE_FULL_UNPAID = 3
    COURSE_ACCESS_TYPE_NONE = 4

    COURSE_ACCESS_TYPES = (
        (COURSE_ACCESS_TYPE_TRIAL, 'Пробный доступ'),
        (COURSE_ACCESS_TYPE_FULL_PAID, 'Оплаченный доступ'),
        (COURSE_ACCESS_TYPE_FULL_UNPAID, 'Полный неоплаченный доступ'),
        (COURSE_ACCESS_TYPE_NONE, 'Без доступа'),
    )

    AVAILABLE_ACCESS_TYPES_FULL = (
        COURSE_ACCESS_TYPE_FULL_PAID,
        COURSE_ACCESS_TYPE_FULL_UNPAID
    )

    AVAILABLE_ACCESS_TYPES = (
        *AVAILABLE_ACCESS_TYPES_FULL,
        COURSE_ACCESS_TYPE_TRIAL
    )

    BLOCK_REASON_FAST_PASSAGE = 1
    BLOCK_REASONS = (
        (BLOCK_REASON_FAST_PASSAGE, 'За сутки было пройдено две темы курса'),
    )


class AccessBase(models.Model, AccessStatuses):
    """
    Базовй класс для получения доступа к любой модели из courses-app
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        'Статус', choices=AccessStatuses.COURSES_STATUSES, default=AccessStatuses.COURSES_STATUS_BLOCK
    )
    date_created = models.DateTimeField('Дата создаения фрагмента', auto_now=True)
    date_completed = models.DateTimeField('Дата завершения', null=True, blank=True)
    block_reason = models.PositiveIntegerField(
        'Причина блокировки', choices=AccessStatuses.BLOCK_REASONS, null=True, blank=True
    )

    class Meta:
        abstract = True


class AccessManagerBase(models.Manager):
    """
    Базовая модель менеджера для управления доступом к курсам
    """

    @abstractmethod
    def set_trial(self, *args, **kwargs) -> typing.Any:
        """
        Обязательный метод для переопределения во всех наследуемых менеджерах
        Требуется для определения зависимостей и связей между бесплатным доступом к курсу
        :param args: Аргументы для метода
        :param kwargs: Ключевые аргументы для метода
        """
        pass

    @abstractmethod
    def check_permission(self, *args, **kwargs) -> bool:
        """
        Метод который проверяет необходимые доступы к моделям courses-app
        :param args: Аргументы для метода
        :param kwargs: Ключевые аргументы для метода
        """
        pass

    def get_status(self, obj: models.Model, user: User) -> int:
        """
        Метод возвращает статус доступа к модели из courses-app
        :param obj: Объект к которому проверяется доступ
        :param user: Объект пользователя
        """
        access_model = self.model.objects.filter(**{self._get_obj_name(obj): obj, 'user': user}).first()

        if access_model is not None:
            return access_model.status
        return AccessBase.COURSES_STATUS_BLOCK

    def set_status(self, obj: models.Model, user: User, status: int) -> typing.Optional[models.Model]:
        """
        Метод обновляет статус прохождения курса пользователем
        :param obj: Некоторый объект из courses-app
        :param user: Пользователь
        :param status: Статус доступа к курсу
        :return: Обновленная модель obj: models.Model
        """
        model = self.filter(**{self._get_obj_name(obj): obj, 'user': user}).first()
        if model is None:
            return None

        update_fields = ['status']
        model.status = status

        if status == AccessBase.COURSES_STATUS_COMPLETED:
            model.date_completed = timezone.now()
            update_fields.append('date_completed')

        return model.save(update_fields=update_fields)

    def _get_obj_name(self, obj):
        return self._to_snake_case(obj.__class__.__name__)

    def set_access(self, **kwargs) -> models.Model:
        """
        Базовый метод для добавления доступа к модели через менеджер
        :param kwargs: Ключевые аргументы для добавления
        :return: models.Model
        """
        return self.model.objects.get_or_create(**kwargs)

    @staticmethod
    def _to_snake_case(string: str) -> str:
        """
        Example: CourseTheme —> course_theme
        :param string: Любой текст
        :return: Текст в формате snake_case
        """
        snake_string = ''
        for id_, char in enumerate(string):
            if char.isupper() and id_ != 0:
                snake_string += '_'

            snake_string += char.lower()
        return snake_string
