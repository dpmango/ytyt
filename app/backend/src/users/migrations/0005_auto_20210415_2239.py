# Generated by Django 3.1.7 on 2021-04-15 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_user_reviewers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_confirmed',
            field=models.BooleanField(default=False, verbose_name='Email подтвержден'),
        ),
    ]