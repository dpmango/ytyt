from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from courses_access.models import Access


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    filter_horizontal = ('manual_access', )
    readonly_fields = ('date_created', 'date_updated')

    fieldsets = (
        (_('Основная информация'), {
            'fields': (
                'user',
                'course',
                'status',
                'access_type',
                'date_created',
                'date_updated',
                'date_completed',
            )
        }),
        (_('Блокировка'), {
            'fields': (
                'block_reason',
            ),
        }),
        (_('Доступы'), {
            'fields': (
                'manual_access',
            ),
        }),
    )
