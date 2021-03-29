from django.contrib import admin
from courses.models import Course, CourseTheme, CourseLesson, LessonFragment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseTheme)
class CourseThemeAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseLesson)
class CourseLessonAdmin(admin.ModelAdmin):
    pass


@admin.register(LessonFragment)
class LessonFragmentAdmin(admin.ModelAdmin):
    pass
