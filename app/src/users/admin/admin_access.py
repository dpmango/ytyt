from django.contrib import admin
from users.mixins import CourseAccess, CourseThemeAccess, CourseLessonAccess


@admin.register(CourseAccess)
class CourseAccessAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseThemeAccess)
class CourseThemeAccessAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseLessonAccess)
class CourseLessonAccessAdmin(admin.ModelAdmin):
    pass
