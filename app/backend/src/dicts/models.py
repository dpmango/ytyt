from django.db import models


class DictsManagerObjects(models.Manager):
    pass


class DictsManager(models.Manager):

    def from_email(self) -> str:
        return self.get(key=self.model.DEFAULT_FROM_EMAIL).value

    def admin_email(self) -> str:
        return self.get(key=self.model.DEFAULT_ADMIN_EMAIL).value

    def support_email(self) -> str:
        return self.get(key=self.model.DEFAULT_SUPPORT_EMAIL).value


class Dicts(models.Model):
    DEFAULT_FROM_EMAIL = 'DEFAULT_FROM_EMAIL'
    DEFAULT_ADMIN_EMAIL = 'DEFAULT_ADMIN_EMAIL'
    DEFAULT_SUPPORT_EMAIL = 'DEFAULT_SUPPORT_EMAIL'
    DEFAULT_MENTOR_EMAIL = 'DEFAULT_MENTOR_EMAIL'
    DEFAULT_EDUCATOR_EMAIL = 'DEFAULT_EDUCATOR_EMAIL'
    DEFAULT_PASSWORD_ROLES = 'DEFAULT_PASSWORD_ROLES'

    DEFAULTS = {
        DEFAULT_FROM_EMAIL: (
            'YtYt.ru <noreply@mail.ytyt.ru>', 'Стандартный email для отправления писем',
        ),
        DEFAULT_ADMIN_EMAIL: (
            'admin@ytyt.ru', 'Стандартный email администратора',
        ),
        DEFAULT_SUPPORT_EMAIL: (
            'support@ytyt.ru', 'Стандартный email для роли суппорта',
        ),
        DEFAULT_MENTOR_EMAIL: (
            'mentor@ytyt.ru', 'Стандартный email для роли наставника',
        ),
        DEFAULT_EDUCATOR_EMAIL: (
            'educator@ytyt.ru', 'Стандартный email для роли преподавателя',
        ),
        DEFAULT_PASSWORD_ROLES: (
            'admin', 'Стандартный пароль для входа для дефолтной роли',
        ),
    }

    key = models.CharField('Ключ', max_length=120)
    value = models.CharField('Значение', max_length=300)
    description = models.CharField('Описание', max_length=100, null=True, blank=True)

    defaults = DictsManager()
    objects = DictsManagerObjects()
