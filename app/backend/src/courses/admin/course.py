from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from courses.models import Course, CourseTheme


class CourseThemeInline(SortableInlineAdminMixin, admin.TabularInline):
    model = CourseTheme
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'cost', 'date_created', 'date_updated')
    exclude = ('order', )
    ordering = (
        'cost', 'date_created', 'date_updated',
    )
    inlines = (CourseThemeInline, )
