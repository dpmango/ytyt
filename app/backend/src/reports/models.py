from django.db import models
from reports.configs import CONFIG


class Report(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Отчеты'
        verbose_name = 'Отчет'

    def __str__(self):
        return CONFIG[self.title]['meta']['ru']
