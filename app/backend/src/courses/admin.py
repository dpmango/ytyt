from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from courses.forms import CourseLessonCreationForm
from courses.models import Course, CourseTheme, CourseLesson, LessonFragment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseTheme)
class CourseThemeAdmin(SortableAdminMixin, admin.ModelAdmin):
    exclude = ('order', )


@admin.register(CourseLesson)
class CourseLessonAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = CourseLessonCreationForm
    exclude = ('order',)


@admin.register(LessonFragment)
class LessonFragmentAdmin(admin.ModelAdmin):
    pass
