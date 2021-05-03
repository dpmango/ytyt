from django.contrib import admin

from courses.forms import CourseLessonCreationForm
from courses.models import CourseLesson
from courses_access.tasks import update_user_access
from courses_access.utils import get_course_from_struct


@admin.register(CourseLesson)
class CourseLessonAdmin(admin.ModelAdmin):
    form = CourseLessonCreationForm

    list_display = ('title', 'date_created', 'date_updated')
    list_select_related = ('course_theme',)
    list_filter = ('course_theme',)
    list_per_page = 15

    exclude = ('order',)
    search_fields = (
        'description',
        'title',
        'content',
    )

    def save_model(self, request, obj, form, change):
        """
        Переопределенный метод дополнительно обновляет доступы к структурам данных для пользователя
        """
        course_id = get_course_from_struct(obj)
        update_user_access(course_id=course_id)

        return super().save_model(request, obj, form, change)
