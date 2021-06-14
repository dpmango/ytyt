import os

from django.conf import settings
from django.contrib import admin

from files.api.serializers import DefaultFileSerializer
from files.models import File, CourseFile


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display_links = ('id', 'date_created', 'file_name')
    list_display = ('id', 'user', 'file_name', 'date_created', 'content_url')

    @staticmethod
    def content_url(obj: File):
        return obj.generate_url(settings.BASE_URL)

    def save_model(self, request, obj, form, change):
        content = obj.content

        _, file_name = os.path.split(content.name)
        _, file_extension = os.path.splitext(file_name)

        if file_extension in DefaultFileSerializer.Meta.image_extensions:
            type_ = File.TYPE_IMAGE
        else:
            type_ = File.TYPE_FILE

        obj.type = type_
        obj.file_name = file_name

        return super().save_model(request, obj, form, change)


@admin.register(CourseFile)
class CourseFileAdmin(admin.ModelAdmin):
    list_display_links = ('id',)
    list_display = ('id', 'content_url')

    @staticmethod
    def content_url(obj: File):
        return obj.generate_url(settings.BASE_URL)