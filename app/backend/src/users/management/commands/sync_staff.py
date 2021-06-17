from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from loguru import logger

from dicts.models import Dicts
from users import permissions
from users.models import User


class Command(BaseCommand):
    help = 'Sync database permissions'

    _PATTERN_DEFAULT_EMAIL = 'DEFAULT_%s_EMAIL'

    def handle(self, *args, **kwargs):
        groups_sync = getattr(permissions, 'GROUPS_SYNC_DEFAULTS')
        default_password = Dicts.objects.filter(key='DEFAULT_PASSWORD_ROLES').first()

        if not default_password:
            raise Exception('Заполните дефолтный пароль для ролей')

        for group_id, group_name in groups_sync:
            group = Group.objects.get(id=group_id)
            default_email = Dicts.objects.filter(key=self._PATTERN_DEFAULT_EMAIL % group_name).first()

            if not default_email:
                raise Exception('Заполните дефолтный email для группы %s' % group)

            if User.objects.filter(groups__in=[group]).exists():
                continue

            default_email = default_email.value
            user, is_created = User.objects.get_or_create(
                email=default_email, is_staff=True, is_active=True
            )

            if is_created:
                logger.info('sync default group_id=%s, group_name=%s, email=%s' % (group_id, group, default_email))
                user.set_password(default_password.value)
                user.groups.add(group)
                user.save()
