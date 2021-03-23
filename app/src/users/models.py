from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users import permissions


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


class User(AbstractBaseUser, PermissionsMixin):

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
    email_confirmed = models.BooleanField(default=False)

    avatar = models.ImageField('Фотография', upload_to='avatars', default='static/default_avatar.png')
    last_name = models.CharField('Фамилия', max_length=255, blank=False, null=True)
    first_name = models.CharField('Имя', max_length=255, blank=False, null=True)
    middle_name = models.CharField('Отчество', max_length=255, blank=True, null=True)

    gender = models.PositiveIntegerField('Пол', choices=GENDERS, default=GENDER_UNKNOWN)

    birthday = models.DateField('Дата рождения', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=64, blank=True, null=True)

    objects = UserManager()

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

    def get_group_id(self):
        if self.is_superuser:
            group_ids = [permissions.GROUP_ADMINISTRATOR]
        else:
            group_ids = [group.id for group in self.groups.all()]
        return group_ids[0] if len(group_ids) > 0 else None

    def get_group_ids(self):
        if self.is_superuser:
            group_ids = [permissions.GROUP_ADMINISTRATOR]
        else:
            group_ids = [group.id for group in self.groups.all()]
        return group_ids

    def get_group_title(self):
        if self.is_superuser:
            group_ids = [permissions.GROUP_ADMINISTRATOR]
        else:
            group_ids = [group.id for group in self.groups.all()]

        group_title = 'Без группы'
        for group_id in group_ids:
            group_info = list(filter(lambda x: x[0] == group_id, permissions.GROUPS))
            if len(group_info):
                group_title = group_info[0][1]
                break
        return group_title

