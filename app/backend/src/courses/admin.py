from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from courses.forms import CourseLessonCreationForm
from courses.models import Course, CourseTheme, CourseLesson, LessonFragment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'cost', 'date_created', 'date_updated')
    exclude = ('order', )
    ordering = (
        'cost', 'date_created', 'date_updated',
    )


@admin.register(CourseTheme)
class CourseThemeAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('get_course_title', 'title', 'date_created', 'date_updated')
    list_select_related = ('course',)
    list_display_links = ('title', )
    list_filter = ('course',)
    list_per_page = 15
    exclude = ('order', )

    def get_course_title(self, obj: CourseTheme):
        return obj.course.title
    get_course_title.short_description = 'Название курса'


@admin.register(CourseLesson)
class CourseLessonAdmin(SortableAdminMixin, admin.ModelAdmin):
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

    def get_theme_title(self, obj: LessonFragment):
        return obj.course_lesson.course_theme.title
    get_theme_title.short_description = 'Название Темы'
