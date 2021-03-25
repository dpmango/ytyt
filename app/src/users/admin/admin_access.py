from django.contrib import admin
from users.mixins import CourseAccess, CourseBlockAccess, CourseBlockLessonAccess


@admin.register(CourseAccess)
class CourseAccessAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseBlockAccess)
class CourseBlockAccessAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseBlockLessonAccess)
class CourseBlockLessonAccessAdmin(admin.ModelAdmin):
    pass
