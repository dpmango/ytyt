import typing

from django.conf import settings
from django.db import transaction
from django.forms.models import model_to_dict
from django.utils import timezone
from loguru import logger
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST

from courses_access.models import Access
from payment.models import Payment
from providers.tinkoff.contrib import Tinkoff, tinkoff_client


class PaymentException(APIException):
    status_code = HTTP_400_BAD_REQUEST


class PaymentLayout:

    def __init__(self, c: Tinkoff):
        self.c = c
        self.errors: typing.Optional[dict] = None

    def is_valid(self, raise_exception: bool = None):
        if not self.errors or len(self.errors) == 0:
            return True

        if raise_exception:
            raise PaymentException(self.errors)
        return False

    def receive(self, raw_payment: dict):

        order_id = raw_payment.get('OrderId')
        status = raw_payment.get('Status')

        try:
            payment = Payment.objects.get(id=order_id)
        except Payment.DoesNotExist as e:
            logger.info('[payment-layout][receive] err=%s' % (e, ))
            return

        payment.status = status
        payment.save(update_fields=['status', 'date_updated'])

        if status == Tinkoff.STATUS_AUTHORIZED:
            self.receive_authorized(payment)

        elif status == Tinkoff.STATUS_CONFIRMED:
            self.receive_confirmed(payment)

    def receive_authorized(self, payment: Payment):
        self.confirm(payment)

    def init(self, payment: Payment) -> typing.Optional[str]:
        """
        Метод инициализирует платеж
        :param payment: Объект платедки с базовой инфомрацией
        :return: Ссылка для оплаты
        """
        init_data = self.c.init(
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

        if status == Tinkoff.STATUS_REJECTED:
            self.errors = {'detail': init_data.get('Details'), 'error_code': init_data.get('ErrorCode')}
            logger.info('[payment-layout][init] {detail}, {error_code}'.format(**self.errors))
            return None

        elif status == Tinkoff.STATUS_NEW:
            return init_data.get('PaymentURL')

        raise Exception({
            'detail': 'У оплаты пришел странный статус — %s' % (status,),
            'context': {
                'init_data': init_data, 'payment': model_to_dict(payment),
            }
        })

    @staticmethod
    def receive_confirmed(payment: Payment) -> None:
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

    def confirm(self, payment: Payment) -> None:
        """
        Метод предоставляет доступ к курсу после оплаты
        :param payment: Объект платежки
        """

        confirm_data = self.c.confirm(
            Amount=payment.amount,
            OrderId=str(payment.id),
            Description=payment.course.description,
        )

        status = confirm_data.get('Status')

        if status == Tinkoff.STATUS_REJECTED:
            payment.status = status
            payment.save(update_fields=['status', 'date_updated'])

            self.errors = {'detail': confirm_data.get('Details'), 'error_code': confirm_data.get('ErrorCode')}
            logger.info('[payment-layout][confirm] {detail}, {error_code}'.format(**self.errors))

            return None

        elif status == Tinkoff.STATUS_CONFIRMED:
            self.receive_confirmed(payment)
            return None

        raise Exception({
            'detail': 'У подтверждения пришел странный статус — %s' % (status,),
            'context': {
                'init_data': confirm_data, 'payment': model_to_dict(payment),
            }
        })


payment_layout = PaymentLayout(
    c=tinkoff_client
)
