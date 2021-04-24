import random
import typing

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import PermissionsMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail import ImageField

from users import permissions
from users.mixins import ReviewersMixins
from users.utils import method_cache_key


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    @staticmethod
    def check_status_online(user_id: int) -> bool:
        return bool(cache.get(method_cache_key(cache_prefix='users__online', user_id=user_id)))

    @staticmethod
    def set_status_online(user_id: int) -> None:
        cache.set(method_cache_key(cache_prefix='users__online', user_id=user_id), 1)

    @staticmethod
    def set_status_offline(user_id: int) -> None:
        cache.set(method_cache_key(cache_prefix='users__online', user_id=user_id), 0)


class ReviewersManager(models.Manager):

    def get_less_busy_educator(self) -> typing.Optional['User']:
        """
        Метод вернет наиболее свободного преподавателя, который НЕ является обычным ревьюером
        """
        educator_group = Group.objects.get(pk=permissions.GROUP_EDUCATOR)

        reviewers = self.filter(groups=educator_group, is_active=True, is_staff=True, reviewer__isnull=True)
        reviewers = reviewers.prefetch_related('reviewer')

        return self._hyperbolic_distribution(reviewers)

    def get_less_busy(self) -> typing.Optional['User']:
        """
        Метод вернет наиболее свободного ревьюера, который НЕ является преподавателем
        """
        educator_group = Group.objects.get(pk=permissions.GROUP_EDUCATOR)

        reviewers = self.filter(~Q(groups=educator_group), is_active=True, is_staff=True, reviewer__isnull=True)
        reviewers = reviewers.prefetch_related('reviewer')

        return self._hyperbolic_distribution(reviewers)

    @staticmethod
    def _hyperbolic_distribution(queryset: typing.List['User']) -> typing.Optional['User']:
        """
        Метод использует функцию-гиперболу для получения веса распределения для преподавателя
        - Чем меньше студентов у препода, тем выше вес
        - Если у пользователя нет студентов, то ему отдается приоритет
        :param queryset: Выборка реквьюеров
        """
        random.seed(timezone.now())

        if len(queryset) == 0:
            return None

        hyperbola = lambda x: 1 / (x if x != 0 else .001)
        queryset_weights = list(map(lambda reviewer: hyperbola(reviewer.user_set.count() / 10), queryset))
        return random.choices(queryset, weights=queryset_weights)[0]


class User(AbstractBaseUser, PermissionsMixin, ReviewersMixins):

    GENDER_UNKNOWN = 0
    GENDER_FEMALE = 1
    GENDER_MALE = 2
    GENDERS = (
        (GENDER_FEMALE, 'Женский'),
        (GENDER_MALE, 'Мужской'),
        (GENDER_UNKNOWN, 'Не определён'),
    )

    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email_confirmed = models.BooleanField('Email подтвержден', default=False)
    email_notifications = models.BooleanField('Уведомления на почту', default=False)

    avatar = ImageField('Фотография', upload_to='avatars', default='static/default_avatar.jpg')
    last_name = models.CharField('Фамилия', max_length=255, blank=False, null=True)
    first_name = models.CharField('Имя', max_length=255, blank=False, null=True)
    middle_name = models.CharField('Отчество', max_length=255, blank=True, null=True)

    gender = models.PositiveIntegerField('Пол', choices=GENDERS, default=GENDER_UNKNOWN)

    birthday = models.DateField('Дата рождения', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=64, blank=True, null=True)
    github_url = models.URLField('Гитхаб', null=True, blank=True)

    objects = UserManager()
    reviewers = ReviewersManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta(AbstractBaseUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        swappable = 'AUTH_USER_MODEL'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.email

    def get_short_name(self):
        """Return the short name for the user."""
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_group_ids(self):
        if self.is_superuser:
            return [permissions.GROUP_ADMINISTRATOR]
        return [group.id for group in self.groups.all()]

    @property
    def ws_key(self) -> str:
        return 'users__%s' % self.id

    def remove_reviewer(self) -> 'User':
        """
        Метод удаляет ревьюера у пользователя
        """
        self.reviewer = None
        self.save()
        return self
