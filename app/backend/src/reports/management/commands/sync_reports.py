from django.core.management.base import BaseCommand
from loguru import logger
from reports.configs import CONFIG
from reports.models import Report


class Command(BaseCommand):
    help = 'Sync database reports'

    def handle(self, *args, **kwargs):

        for report_title in CONFIG.keys():

            logger.info('[sync-report] title=%s' % report_title)
            Report.objects.update_or_create(title=report_title)
