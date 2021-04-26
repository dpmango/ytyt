from django.contrib import admin
from django.db import models
from markdownx.widgets import AdminMarkdownxWidget

from courses.forms import CourseLessonCreationForm
from courses.models import CourseLesson


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
    #
    # formfield_overrides = {
    #     models.TextField: {'widget': AdminMarkdownxWidget},
    # }
