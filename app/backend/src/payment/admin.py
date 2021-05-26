from django.contrib import admin
from payment.models import Payment, PaymentCredit


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentCredit)
class PaymentCreditAdmin(admin.ModelAdmin):
    pass
