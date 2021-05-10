from django.contrib import admin

from reports.models import Report
from reports.tasks import generate_users_report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):

    def _generate_users_report(self, _, queryset, **kwargs):
        for report in queryset:
            # generate_users_report.delay(report.title)  # TODO: set
            generate_users_report(report.title)

    _generate_users_report.short_description = 'Сгенерировать отчет'
    actions = [_generate_users_report]
