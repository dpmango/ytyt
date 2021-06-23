from django.contrib import admin
from django.db.models.signals import post_delete

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

    def delete_model(self, request, obj):
        model = super().delete_model(request, obj)
        post_delete.send(instance=None, sender=CourseLesson)
        return model
