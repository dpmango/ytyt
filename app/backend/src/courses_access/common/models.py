import typing
from abc import abstractmethod

from django.db import models
from users.models import User


class AccessBase(models.Model):
    """
    Базовй класс для получения доступа к любой модели из courses-app
    """

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

    def get_status(self, obj: models.Model, user: User, ) -> int:
        """
        Метод возвращает статус доступа к модели из courses-app
        :param obj: Объект к которому проверяется доступ
        :param user: Объект пользователя
        """
        access_model = self.model.objects.filter(**{
            self._to_snake_case(obj.__class__.__name__): obj, 'user': user
        }).first()

        if access_model is not None:
            return access_model.status
        return AccessBase.COURSES_STATUS_BLOCK

    def set_access(self, **kwargs) -> models.Model:
        """
        Базовый метод для добавления доступа к модели через менеджер
        :param kwargs: Ключевые аргументы для добавления
        :return: models.Model
        """
        return self.model.objects.get_or_create(**kwargs)

    def is_accessible(self, **kwargs) -> bool:
        return self.filter(**kwargs).exists()

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
