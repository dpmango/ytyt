from django.core.management import BaseCommand
from loguru import logger

from dicts.models import Dicts


class Command(BaseCommand):
    help = 'Sync default values'

    def handle(self, *args, **kwargs):
        for key, item in Dicts.DEFAULTS.items():

            value, description = item
            dict_, is_created = Dicts.objects.get_or_create(key=key)

            if is_created:
                logger.info('sync default dicts values[%s], key=%s, value=%s' % (description, key, value))

                dict_.value = value
                dict_.description = description
                dict_.save(update_fields=['description', 'value'])
