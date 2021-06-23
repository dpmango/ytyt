from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.db.models.signals import post_save, post_delete

from courses.models import Course
from courses.models import CourseTheme


class CourseThemeInline(SortableInlineAdminMixin, admin.TabularInline):
    model = CourseTheme
    extra = 1
    can_delete = False


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'cost', 'date_created', 'date_updated')
    exclude = ('order', )
    ordering = (
        'cost', 'date_created', 'date_updated',
    )
    inlines = (CourseThemeInline, )

    def save_formset(self, request, form, formset, change):
        data = super().save_formset(request, form, formset, change)

        # Дополнительно инициализируем сигнал для изменения порядка следования элементов
        # Сигнал будет проигнорирован, если ранее были отправлены сигналы с изменениями
        post_save.send(instance=None, sender=CourseTheme)

        return data

    def delete_model(self, request, obj):
        model = super().delete_model(request, obj)
        post_delete.send(instance=None, sender=CourseTheme)
        return model
