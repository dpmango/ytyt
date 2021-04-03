from django.contrib import admin

from courses.forms import CourseLessonCreationForm
from courses.models import Course, CourseTheme, CourseLesson, LessonFragment, CourseAccess


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseTheme)
class CourseThemeAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseLesson)
class CourseLessonAdmin(admin.ModelAdmin):
    form = CourseLessonCreationForm


@admin.register(LessonFragment)
class LessonFragmentAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseAccess)
class CourseAccessAdmin(admin.ModelAdmin):
    pass
