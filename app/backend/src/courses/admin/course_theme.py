from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from courses.admin.course_lesson import CourseLessonCreationForm
from courses.models import CourseTheme, CourseLesson
from courses_access.tasks import update_user_access
from courses_access.utils import get_course_from_struct


class CourseLessonInline(SortableInlineAdminMixin, admin.TabularInline):
    model = CourseLesson
    exclude = ('content', 'description')
    extra = 1
    can_delete = False
    form = CourseLessonCreationForm


@admin.register(CourseTheme)
class CourseThemeAdmin(admin.ModelAdmin):
    list_display = ('get_course_title', 'title', 'date_created', 'date_updated')
    list_select_related = ('course',)
    list_display_links = ('title', )
    list_filter = ('course',)
    list_per_page = 15
    exclude = ('order', )
    inlines = (CourseLessonInline,)

    def get_course_title(self, obj: CourseTheme):
        return obj.course.title
    get_course_title.short_description = 'Название курса'

    def save_model(self, request, obj, form, change):
        """
        Переопределенный метод дополнительно обновляет доступы к структурам данных для пользователя
        """
        if obj.order in (None, 0):
            max_order = CourseTheme.objects.order_by('-order').first()
            obj.order = max_order.order + 1 if max_order else 0

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
