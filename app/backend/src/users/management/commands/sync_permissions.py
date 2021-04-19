from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError
from loguru import logger

from users import permissions


class Command(BaseCommand):
    help = 'Sync database permissions'

    def handle(self, *args, **kwargs):

        if not hasattr(permissions, 'GROUPS'):
            raise CommandError('invalid LOGIN_PERMISSIONS_MODULE, GROUPS list not found')

        if not hasattr(permissions, 'GROUP_RIGHTS'):
            raise CommandError('invalid LOGIN_PERMISSIONS_MODULE, GROUP_RIGHTS dict not found')

        groups = getattr(permissions, 'GROUPS')
        group_rights = getattr(permissions, 'GROUP_RIGHTS')

        for group_id, group_name in groups:
            logger.info('create group %s' % group_name)
            group = Group()
            group.id = group_id
            group.name = group_name
            group.save()

            if group_id in group_rights:
                logger.info('clear group %s rights' % group_name)
                group.permissions.clear()

                for group_permission in group_rights[group_id]:
                    app_label, permission_codename = group_permission.split('.')
                    group.permissions.add(
                        Permission.objects.get(content_type__app_label=app_label, codename=permission_codename)
                    )

                    logger.info('added %s to %s' % (group_permission, group_name))
