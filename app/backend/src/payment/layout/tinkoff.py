import typing

from django.conf import settings
from django.db import transaction
from django.forms.models import model_to_dict
from django.utils import timezone
from loguru import logger

from courses_access.models import Access
from payment.layout.core import Layout
from payment.models import Payment
from providers.tinkoff.contrib import Tinkoff, tinkoff_client

__all__ = ('PaymentLayout', )


class PaymentLayout(Layout):
    _cli = tinkoff_client

    def receive(self, raw_payment: dict):
        super().receive(raw_payment)

        order_id = raw_payment.get('OrderId')
        payment_id = raw_payment.get('PaymentId')
        status = raw_payment.get('Status')

        try:
            payment = Payment.objects.get(id=order_id)
            prev_status = payment.status
        except Payment.DoesNotExist as e:
            logger.info('[%s][receive] err=%s' % (self._class, e,))
            return

        # Если платеж был подтвержден ранее, то пропускаем
        if payment.status == Tinkoff.STATUS_CONFIRMED:
            return None

        with transaction.atomic():
            payment.status = status
            payment.external_payment_id = payment_id
            payment.save(update_fields=['status', 'external_payment_id', 'date_updated'])

            # Если используется двухстайдийная оплата, то придет статус `STATUS_AUTHORIZED`, который нужно будет
            # подтвердить
            # Этот статус учитывается только в том случае, если предыдущий статус был STATUS_3DS_CHECKED,
            # это как сигнал о том, что оплата происходила в две стадии
            if status == Tinkoff.STATUS_AUTHORIZED and prev_status == Tinkoff.STATUS_3DS_CHECKED:
                self.receive_authorized(payment)

            # Если двухстадийная оплата не использовалась, то придет уже подтвержденный статус оплаты
            if status == Tinkoff.STATUS_CONFIRMED:
                self.receive_confirmed(payment)

    def init(self, payment: Payment) -> typing.Optional[str]:
        """
        Метод инициализирует платеж
        Документация — https://www.tinkoff.ru/kassa/develop/api/payments/
        :param payment: Объект платедки с базовой инфомрацией
        :return: Ссылка для оплаты
        """
        init_data = self.cli.init(
            Amount=payment.amount,
            OrderId=str(payment.id),
            Description=payment.course.description,
            DATA=dict(
                Email=payment.user.email,
            ),
            Receipt=dict(
                Email=payment.user.email,
                EmailCompany=settings.DEFAULT_ADMIN_EMAIL,
                Taxation=Tinkoff.TAXATION_USN_INCOME,
                Items=[
                    dict(
                        Name=payment.course.title,
                        Price=payment.amount,
                        Quantity=1.00,
                        Amount=payment.amount,
                        PaymentMethod=Tinkoff.PAYMENT_METHOD_FULL_PAYMENT,
                        Tax=Tinkoff.TAX_NONE,
                    ),
                ],
            ),
        )

        status = init_data.get('Status')

        payment.status = status
        payment.save(update_fields=['status', 'date_updated'])

        error = self.cli.is_error(init_data)
        if error is not None:
            self.errors = error
            logger.info('[{_class}][init] {error}'.format(_class=self._class, error=self.errors))

        if status == Tinkoff.STATUS_REJECTED:
            self.errors = {'detail': init_data.get('Details'), 'error_code': init_data.get('ErrorCode')}
            logger.info('[{_class}][init] {detail}, {error_code}'.format(_class=self._class, **self.errors))
            return None

        if status == Tinkoff.STATUS_NEW:
            return init_data.get('PaymentURL')

        raise Exception({
            'detail': 'У оплаты пришел странный статус — %s' % (status,),
            'context': {
                'init_data': init_data, 'payment': model_to_dict(payment),
            }
        })

    def receive_authorized(self, payment: Payment, **kwargs) -> None:
        """
        Метод подтверждает оплату и предоставляет доступ, если все ок
        :param payment: Объект платежки
        """
        confirm_data = self.cli.confirm(PaymentId=str(payment.external_payment_id))
        status = confirm_data.get('Status')

        if status == Tinkoff.STATUS_REJECTED:
            payment.status = status
            payment.save(update_fields=['status', 'date_updated'])

            self.errors = {'detail': confirm_data.get('Details'), 'error_code': confirm_data.get('ErrorCode')}
            logger.info('[{_class}][confirm] {detail}, {error_code}'.format(_class=self._class, **self.errors))

            return None

        elif status == Tinkoff.STATUS_CONFIRMED:
            self.receive_confirmed(payment)
            return None

        self.errors = {
            'detail': 'У подтверждения пришел странный статус — %s' % (status,),
            'context': {
                'confirm_data': confirm_data, 'payment': model_to_dict(payment),
            }
        }
        logger.info('[{_class}][confirm] {detail}, {error_code}'.format(_class=self._class, **self.errors))

    @staticmethod
    def receive_confirmed(payment: Payment, **kwargs) -> None:
        """
        Метод для подтверждения оплаты
        :param payment: Объект платежки
        """
        with transaction.atomic():
            # Меняем статус оплаты
            payment.status = Tinkoff.STATUS_CONFIRMED
            payment.date_payment = timezone.now()
            payment.save(update_fields=['status', 'date_updated', 'date_payment'])

            # Переназначаем ревьюера
            payment.user.re_elect_reviewer()

            # Предоставляем доступ к курсу
            access = payment.user.access_set.filter(course=payment.course).first()
            access.access_type = Access.COURSE_ACCESS_TYPE_FULL_PAID
            access.save()
