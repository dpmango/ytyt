from django.contrib import admin
from .models import Course, CourseBlock, CourseBlockLesson, CTest
from martor.widgets import AdminMartorWidget
from django.db import models

@admin.register(CTest)
class CTestAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseBlock)
class CourseBlockAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseBlockLesson)
class CourseBlockLessonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }