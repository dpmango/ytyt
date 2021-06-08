import typing

from django.db import transaction
from django.forms import model_to_dict
from django.utils import timezone
from loguru import logger

from courses_access.models import Access
from payment.layout.core import Layout
from payment.models import PaymentCredit
from providers.mailgun.mixins import EmailNotification
from providers.tinkoff_credit.contrib import tinkoff_credit_client, TinkoffCredit
from users.shortcuts import replace_educator_to_reviewer

__all__ = ('PaymentCreditLayout', )


class PaymentCreditLayout(Layout):
    _cli = tinkoff_credit_client

    def receive(self, raw_payment_credit: dict):
        super().receive(raw_payment_credit)

        pk = raw_payment_credit.get('id')
        status = raw_payment_credit.get('status')

        if not status or not pk:
            return

        try:
            payment_credit = PaymentCredit.objects.get(pk=pk)
        except PaymentCredit.DoesNotExist as e:
            logger.info('[%s][receive] err=%s' % (self._class, e,))
            return

        # Если кредит был подтвержден ранее, то пропускаем
        if payment_credit.status == TinkoffCredit.STATUS_SIGNED:
            return None

        with transaction.atomic():
            payment_credit.status = status
            payment_credit.save(update_fields=['status', 'date_updated'])

            if status == TinkoffCredit.STATUS_SIGNED:
                self.receive_signed(payment_credit)

            elif status == TinkoffCredit.STATUS_REJECTED:
                self.receive_rejected(payment_credit)

    @staticmethod
    def receive_signed(payment_credit: PaymentCredit) -> None:
        """
        Метод подтверждает выдачу кредита —> можно предоставить доступ к курсу
        :param payment_credit: Объект с информаций о займе
        """
        with transaction.atomic():
            # Меняем статус оплаты
            payment_credit.status = TinkoffCredit.STATUS_SIGNED
            payment_credit.date_approval = timezone.now()
            payment_credit.save(update_fields=['status', 'date_updated', 'date_approval'])

            # Переназначаем ревьюера
            replace_educator_to_reviewer(payment_credit.user)

            # Предоставляем доступ к курсу
            access = payment_credit.user.access_set.filter(course=payment_credit.course).first()
            access.set_access_full_paid()

    @staticmethod
    def receive_rejected(payment_credit: PaymentCredit) -> None:
        """
        Метод уведомляет админа по отказу в рассрочке для пользователя
        :param payment_credit: Объект займа
        """
        mailgun = EmailNotification(
            subject_template_raw='Отказ в рассрочке',
            email_template_raw='Пользователю отказали в рассрочке.\nID: {id},\nИмя: {first_name},\nEmail: {email}',
        )
        mailgun.send_mail(context=model_to_dict(payment_credit.user))

    def create(self, payment_credit: PaymentCredit) -> typing.Optional[str]:
        """
        Метод для создания заявки
        Документация — https://forma.tinkoff.ru/docs/credit/help/methods/?type=api&method=create
        :param payment_credit: Объект займа
        """
        creation_data = self.cli.create_demo(
            sum=payment_credit.amount,
            orderNumber=payment_credit.pk,
            promoCode=payment_credit.promo_code,
            demoFlow="sms",
            items=[
                dict(
                    name=payment_credit.course.title,
                    price=payment_credit.amount,  # Данные по прайсу в рамках кредитования отправляются НЕ в копейках
                    quantity=1,
                ),
            ],
            values=dict(
                contact=dict(
                    fio=dict(
                        lastName=payment_credit.user.last_name,
                        firstName=payment_credit.user.first_name,
                    ),
                    email=payment_credit.user.email,
                )
            )
        )

        error = self.cli.is_error(creation_data)
        if error is not None:
            self.errors = {'error': error}
            logger.info('[{_class}][init] {error}'.format(_class=self._class, **self.errors))
            return None

        _id = creation_data.get('id')
        link = creation_data.get('link')

        if _id == link is None:
            self.errors = {'creation_data': creation_data}
            logger.info('[{_class}][init] {creation_data}'.format(_class=self._class, **self.errors))
            return None

        payment_credit.external_payment_id = _id
        payment_credit.save(update_fields=['external_payment_id', 'date_updated'])

        return link
