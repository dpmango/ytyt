import os
import zipfile
import typing as t

import chardet
from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from files.models import CourseFile
from django.conf import settings


class FilesFomRarCreationForm(forms.ModelForm):
    tree = forms.CharField(widget=forms.Textarea, label='Дерево файлов')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if instance := kwargs.get('instance'):
            tree, rows = self.get_tree(instance)

            self.fields['tree'].strip = False
            self.fields['tree'].initial = tree
            self.fields['tree'].widget.attrs['readonly'] = True
            self.fields['tree'].widget.attrs['rows'] = rows
            self.fields['tree'].widget.attrs['cols'] = 120

    @staticmethod
    def get_tree(obj: CourseFile) -> t.Tuple[str, int]:
        """
        Метод вернет дерево файлов для курса
        :param obj: Объект файла курса с архивом
        :return: Метод вернет строки для отображения и общее количество строк
        """
        path = os.path.dirname(obj.content.file.name)
        tree = []

        for dir_path, dir_names, filenames in os.walk(path):

            directory_level = dir_path.replace(path, '')
            directory_level = directory_level.count(os.sep)

            indent = ' ' * 4
            tree.append('%s%s/' % (indent * directory_level, os.path.basename(dir_path)))

            for file in filenames:
                tree.append('%s%s' % (indent * (directory_level + 1), file))

        return '\n'.join(tree), len(tree)

    def clean(self):
        if 'content' in self.changed_data:
            content = self.cleaned_data['content']

            if isinstance(content, InMemoryUploadedFile):
                try:
                    ipynb_file_file_extension = content.name.split('.')[-1]
                except IndexError:
                    raise ValidationError('У файла `%s` не указано расширение' % content.name)
                else:
                    if ipynb_file_file_extension not in self.Meta.allowed_zip_file_extension:
                        raise ValidationError('Расширение `.%s` не поддерживется' % ipynb_file_file_extension)

    def save(self, commit=True):
        course_file = super().save(commit)
        CourseFile.objects.exclude(pk=course_file.pk).delete()
        return course_file

    @classmethod
    def save_files(cls, obj: CourseFile) -> None:
        """
        Метод сохраняет файлы из архива
        :param obj: объект файла с архивом
        """
        with zipfile.ZipFile(obj.content.file.name) as zip_archive:

            for zip_file in zip_archive.filelist:
                file_name = zip_file.filename

                if zip_file.flag_bits & 0x800 == 0:
                    filename_bytes = file_name.encode('437')

                    guessed_encoding = chardet.detect(filename_bytes)['encoding'] or 'cp1252'
                    file_name = filename_bytes.decode(guessed_encoding, 'replace')

                if any(item.lower() in file_name.lower() for item in cls.Meta.not_allowed_file_name):
                    continue

                *_, file_expansion = os.path.splitext(file_name)
                if not file_expansion:
                    continue

                os.makedirs(os.path.join(cls.Meta.uploads_root, os.path.dirname(file_name)), exist_ok=True)

                with open(os.path.join(cls.Meta.uploads_root, file_name), 'wb') as file:
                    file.write(zip_archive.read(zip_file.filename))

    class Meta:
        model = CourseFile
        fields = '__all__'

        allowed_zip_file_extension = ('zip', )
        not_allowed_file_name = ('DS_Store', 'MACOSX')
        uploads_root = os.path.join(settings.MEDIA_ROOT, settings.MARKDOWNX_MEDIA_PATH)
