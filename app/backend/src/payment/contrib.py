from providers.tinkoff.contrib import Tinkoff, tinkoff_client
from payment.models import Payment
from django.conf import settings


class PaymentLayout:

    def __init__(self, cli: Tinkoff):
        self.cli = cli

    def init(self, payment: Payment):

        data = self.cli.init(
            Amount=payment.amount,
            OrderId=str(payment.id),
            Description=payment.course.description,
            DATA=dict(
                Email=payment.user.email,
            ),
            Receipt=dict(
                Email=payment.user.email,
                EmailCompany=settings.DEFAULT_ADMIN_EMAIL,
                Taxation=Tinkoff.TAXATION_OSN  # TODO: Узнать
            ),
            Items=list(
                dict(
                    Name=payment.course.title,
                    Price=payment.amount,
                    Quantity=1.00,
                    Amount=payment.amount,
                    PaymentMethod=Tinkoff.PAYMENT_METHOD_FULL_PAYMENT,  # TODO: Узнать
                    Tax=Tinkoff.TAX_NONE,  # TODO: Узнать
                ),
            ),
        )








payment_layout = PaymentLayout(
    cli=tinkoff_client
)
