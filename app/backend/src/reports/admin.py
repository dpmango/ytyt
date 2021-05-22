from django.contrib import admin

from reports.models import Report
from reports.tasks import generate_users_report
from django.conf import settings


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):

    def _generate_users_report(self, _, queryset, **kwargs):
        for report in queryset:
            if settings.IS_PRODUCTION:
                generate_users_report.delay(report.title)
            else:
                generate_users_report(report.title)

    _generate_users_report.short_description = 'Сгенерировать отчет'
    actions = [_generate_users_report]

    readonly_fields = ('title', )
