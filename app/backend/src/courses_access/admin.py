import json

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from courses_access.models import Access


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    filter_horizontal = ('manual_access', )
    readonly_fields = (
        'date_created',
        'date_updated',
        'course_theme_json',
        'course_lesson_json',
        'lesson_fragment_json',
    )

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
        (_('Доступы в формате json'), {
            'classes': ('collapse', ),
            'fields': (
                ('course_theme_json', 'course_lesson_json', 'lesson_fragment_json')
            ),
        }),
    )

    @staticmethod
    def course_theme_json(obj):
        return json.dumps(obj.course_theme, indent=4, ensure_ascii=False)

    @staticmethod
    def course_lesson_json(obj):
        return json.dumps(obj.course_lesson, indent=4, ensure_ascii=False)

    @staticmethod
    def lesson_fragment_json(obj):
        return json.dumps(obj.lesson_fragment, indent=4, ensure_ascii=False)
