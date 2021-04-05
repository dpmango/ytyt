from django.contrib import admin
from courses_access.models import CourseAccess, CourseThemeAccess, CourseLessonAccess, LessonFragmentAccess


@admin.register(CourseAccess)
class CourseAccessAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseThemeAccess)
class CourseThemeAccessAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseLessonAccess)
class CourseLessonAccessAdmin(admin.ModelAdmin):
    pass


@admin.register(LessonFragmentAccess)
class LessonFragmentAccessAdmin(admin.ModelAdmin):
    pass
