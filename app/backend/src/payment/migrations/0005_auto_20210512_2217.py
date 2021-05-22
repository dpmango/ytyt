# Generated by Django 3.1.7 on 2021-05-12 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_payment_external_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentcredit',
            name='external_payment_id',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='ID платежа во внешней системе'),
        ),
        migrations.AlterField(
            model_name='paymentcredit',
            name='status',
            field=models.CharField(blank=True, choices=[('approved', 'Заявка одобрена'), ('rejected', 'По заявке отказ'), ('canceled', 'Заявка отменена'), ('signed', 'Договор подписан')], max_length=21, null=True, verbose_name='Статус одобрения'),
        ),
    ]
