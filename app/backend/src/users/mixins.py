from django.db import models


class ReviewersMixins(models.Model):
    """
    Миксин-класс для работы с ревьюерами
    """

    reviewer = models.ForeignKey('users.User', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True


class SupportsMixins(models.Model):
    """
    Миксин-класс для работы с суппортами
    """

    support = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, blank=True, null=True, related_name='user_from_support'
    )

    class Meta:
        abstract = True
