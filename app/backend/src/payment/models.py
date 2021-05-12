from django.db import models

from courses.models import Course
from providers.tinkoff.contrib import Tinkoff
from providers.tinkoff_credit.contrib import TinkoffCredit
from users.models import User


class PaymentBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    date_updated = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        abstract = True


class Payment(PaymentBase):
    amount = models.DecimalField('Сумма оплаты в копейках', max_digits=10, decimal_places=2)
    date_payment = models.DateTimeField('Дата оплаты', null=True, blank=True)
    status = models.CharField('Статус платежки', choices=Tinkoff.STATUSES, max_length=21, null=True, blank=True)


class PaymentCredit(PaymentBase):
    amount = models.DecimalField('Сумма оплаты', max_digits=10, decimal_places=2)
    promo_code = models.CharField('Тип кредитного продукта',
                                  choices=TinkoffCredit.PROMO_CODES, null=True, blank=True, max_length=21)
    date_approval = models.DateTimeField('Дата подтверждения заявки', null=True, blank=True)
    status = models.CharField('Статус одобрения', choices=TinkoffCredit.STATUSES, max_length=21, null=True, blank=True)
