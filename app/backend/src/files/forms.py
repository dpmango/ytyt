from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from markdownx.utils import markdownify
from django import forms

from courses.models import CourseLesson, LessonFragment
from courses.utils import html_to_text
from courses.inline_command import InlineCommandExtend
from files.models import CourseFile
import zipfile



class FilesFomRarCreationForm(forms.ModelForm):

    def clean(self):
        if 'content' in self.changed_data:
            content = self.cleaned_data['content']

            if isinstance(content, InMemoryUploadedFile):
                try:
                    ipynb_file_file_extension = content.name.split('.')[-1]
                except IndexError:
                    raise ValidationError('У файла `%s` не указано расширение' % content.name)
                else:
                    if ipynb_file_file_extension not in self.Meta.allowed_file_extension:
                        raise ValidationError('Расширение `.%s` не поддерживется' % ipynb_file_file_extension)

    def save(self, commit=True):

        course_file_obj = super().save(commit)
        CourseFile.objects.exclude(pk=course_file_obj.pk).delete()



        return course_file_obj





    class Meta:
        model = CourseFile
        fields = '__all__'

        allowed_file_extension = ('zip', )
