from django.db import models

from courses.models import Course
from providers.tinkoff.contrib import Tinkoff
from users.models import User


class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    amount = models.DecimalField('Сумма оплаты в копейках', max_digits=10, decimal_places=2)

    date_created = models.DateTimeField('Дата создания платежки', auto_now_add=True)
    date_updated = models.DateTimeField('Дата обновления платежки', auto_now=True)
    date_payment = models.DateTimeField('Дата оплаты', null=True, blank=True)

    status = models.CharField('Статус платежки', choices=Tinkoff.STATUSES, max_length=21, null=True, blank=True)