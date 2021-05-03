from django.contrib import admin

from courses.models import LessonFragment
from courses_access.tasks import update_user_access
from courses_access.utils import get_course_from_struct


@admin.register(LessonFragment)
class LessonFragmentAdmin(admin.ModelAdmin):
    list_display = ('get_theme_title', 'get_lesson_title', 'title', 'date_created', 'date_updated')
    list_select_related = ('course_lesson', 'course_lesson__course_theme')
    list_display_links = ('title', 'date_created', 'date_updated')
    list_filter = ('course_lesson', )
    list_per_page = 10

    search_fields = (
        'course_lesson__description',
        'course_lesson__title',
        'content',
        'title',
    )
    ordering = (
        'course_lesson__course_theme__order',
        'course_lesson__order',
        'date_created',
        'date_updated'
    )

    def get_lesson_title(self, obj: LessonFragment):
        return obj.course_lesson.title
    get_lesson_title.short_description = 'Название урока'
    get_lesson_title.admin_order_field = 'course_lesson__order'

    def get_theme_title(self, obj: LessonFragment):
        return obj.course_lesson.course_theme.title
    get_theme_title.short_description = 'Название Темы'
    get_theme_title.admin_order_field = 'course_lesson__course_theme__order'

    def save_model(self, request, obj, form, change):
        """
        Переопределенный метод дополнительно обновляет доступы к структурам данных для пользователя
        """
        course_id = get_course_from_struct(obj)
        update_user_access(course_id=course_id)

        return super().save_model(request, obj, form, change)
