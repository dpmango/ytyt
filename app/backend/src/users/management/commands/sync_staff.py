from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from loguru import logger

from users import permissions
from users.models import User


class Command(BaseCommand):
    help = 'Sync database permissions'

    def handle(self, *args, **kwargs):
        groups_sync = getattr(permissions, 'GROUPS_SYNC_DEFAULTS_EMAILS')

        for group_id, default_email in groups_sync.items():
            group = Group.objects.get(id=group_id)
            logger.info('sync default group_id=%s, group_name=%s, email=%s' % (group_id, group, default_email))

            if User.objects.filter(groups__in=[group]).exists():
                continue

            user, is_created = User.objects.get_or_create(
                email=default_email,
                is_staff=True,
                is_active=True
            )
            if is_created:
                user.set_password(default_email.split('@')[0])
                user.groups.add(group)
                user.save()
