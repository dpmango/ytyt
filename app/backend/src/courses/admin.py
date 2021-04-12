from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from courses.forms import CourseLessonCreationForm
from courses.models import Course, CourseTheme, CourseLesson, LessonFragment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    exclude = ('order', )


@admin.register(CourseTheme)
class CourseThemeAdmin(SortableAdminMixin, admin.ModelAdmin):
    exclude = ('order', )


@admin.register(CourseLesson)
class CourseLessonAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = CourseLessonCreationForm
    exclude = ('order',)


@admin.register(LessonFragment)
class LessonFragmentAdmin(admin.ModelAdmin):

    list_display = ('get_theme_title', 'get_lesson_title', 'title', 'date_created', 'date_updated')
    list_display_links = ('title', 'date_created', 'date_updated')
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

    list_filter = ('course_lesson', )
    list_per_page = 10

    def get_lesson_title(self, obj: LessonFragment):
        return obj.course_lesson.title
    get_lesson_title.short_description = 'Название урока'

    def get_theme_title(self, obj: LessonFragment):
        return obj.course_lesson.course_theme.title
    get_theme_title.short_description = 'Название Темы'

