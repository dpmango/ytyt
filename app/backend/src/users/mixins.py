from django.db import models
from django.utils.translation import gettext_lazy as _


class ReviewersMixins(models.Model):
    """
    Миксин-класс для работы с пользователем, как с ревьюером
    """

    user_reviewers = models.ManyToManyField(
        'users.User',
        verbose_name=_('Ревьюеры пользователя'),
        blank=True,
        related_name="reviewers_set",
        related_query_name="reviewers",
    )

    class Meta:
        abstract = True
