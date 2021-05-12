from django.core.management.base import BaseCommand
from loguru import logger

from payment.models import Payment
from providers.tinkoff.contrib import tinkoff_client


class Command(BaseCommand):
    help = 'Cancel payment'

    def add_arguments(self, parser):
        parser.add_argument('--payment_id', type=int, help='ID платежа в нашей системе')
        parser.add_argument('--external_payment_id', type=int, help='ID платежа во внешней системе')

    def handle(self, *args, **kwargs):
        payment_id = kwargs.get('payment_id')
        external_payment_id = kwargs.get('external_payment_id')

        if payment_id is not None:
            try:
                payment = Payment.objects.get(id=payment_id)
                external_payment_id = payment.external_payment_id
            except Payment.DoesNotExist:
                logger.info('[cancel-payment] Платежа с таким ID внутри системы не существует')
                return

            logger.info(
                '[cancel-payment] payment_id=%s --> external_payment_id=%s' % (
                    payment_id, external_payment_id
                )
            )

        elif external_payment_id is not None:
            try:
                payment = Payment.objects.get(external_payment_id=external_payment_id)
            except Payment.DoesNotExist:
                logger.info('[cancel-payment] Платежа с таким внешним ID внутри системы не существует')
                return

            logger.info('[cancel-payment] external_payment_id=%s' % external_payment_id)

        else:
            logger.info('[cancel-payment] Нет информации по ID платежа для отмены')
            return

        data = tinkoff_client.cancel(PaymentId=str(external_payment_id))
        if not data:
            logger.debug('[cancel-payment] Не удалось отменить платеж, пришел пустой ответ на запрос')

        status = data.get('Status')

        payment.status = status
        payment.save(update_fields=['status', 'date_updated'])

        logger.info(
            '[cancel-payment] Платеж payment_id=%s, external_payment_id=%s отменен!' % (
                payment.pk, payment.external_payment_id
            )
        )
