from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.db.models.signals import post_save, post_delete

from courses.admin.course_lesson import CourseLessonCreationForm
from courses.models import CourseTheme, CourseLesson


class CourseLessonInline(SortableInlineAdminMixin, admin.TabularInline):
    model = CourseLesson
    exclude = ('content', 'description')
    extra = 1
    can_delete = False
    form = CourseLessonCreationForm


@admin.register(CourseTheme)
class CourseThemeAdmin(admin.ModelAdmin):
    list_display = ('get_course_title', 'title', 'date_created', 'date_updated')
    list_select_related = ('course',)
    list_display_links = ('title', )
    list_filter = ('course',)
    list_per_page = 15
    exclude = ('order', )
    inlines = (CourseLessonInline,)

    def get_course_title(self, obj: CourseTheme):
        return obj.course.title
    get_course_title.short_description = 'Название курса'

    def save_formset(self, request, form, formset, change):
        data = super().save_formset(request, form, formset, change)

        print(formset.changed_objects)

        # Дополнительно инициализируем сигнал для изменения порядка следования элементов
        # Сигнал будет проигнорирован, если ранее были отправлены сигналы с изменениями
        post_save.send(instance=None, sender=CourseLesson)

        return data

    def delete_model(self, request, obj):
        model = super().delete_model(request, obj)
        post_delete.send(instance=None, sender=CourseLesson)
        return model
