from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from courses.models import Course, CourseTheme
from courses_access.tasks import update_user_access
from courses_access.utils import get_course_from_struct


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

    def save_model(self, request, obj, form, change):
        """
        Переопределенный метод дополнительно обновляет доступы к структурам данных для пользователя
        """
        model = super().save_model(request, obj, form, change)

        course_id = get_course_from_struct(obj)
        update_user_access(course_id=course_id)

        return model

    def delete_model(self, request, obj):
        """
        Переопределенный метод дополнительно обновляет доступы к структурам данных для пользователя
        """

        course_id = get_course_from_struct(obj)
        update_user_access(course_id=course_id)

        return super().delete_model(request, obj)
