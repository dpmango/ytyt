from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from loguru import logger

from users.models import User


class Command(BaseCommand):
    help = 'Sync database permissions'

    _DEFAULT_EMAIL = 'admin@admin.ad'

    def handle(self, *args, **kwargs):

        logger.info('sync super admin, email=%s' % self._DEFAULT_EMAIL)
        try:
            User.objects.create_superuser(email=self._DEFAULT_EMAIL, password=settings.SUPER_ADMIN_PASSWORD)
        except IntegrityError:
            pass
