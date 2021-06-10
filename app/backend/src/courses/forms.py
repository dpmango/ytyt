import json

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from markdownx.utils import markdownify

from courses.models import CourseLesson, LessonFragment
from courses.utils import html_to_text
from courses.inline_command import InlineCommandExtend


class CourseLessonCreationForm(forms.ModelForm):

    def clean(self):
        if 'ipynb_file' in self.changed_data:
            ipynb_file = self.cleaned_data['ipynb_file']

            if isinstance(ipynb_file, InMemoryUploadedFile):
                try:
                    ipynb_file_file_extension = ipynb_file.name.split('.')[-1]
                except IndexError:
                    raise ValidationError('У файла `%s` не указано расширение' % ipynb_file.name)
                else:
                    if ipynb_file_file_extension not in self.Meta.allowed_file_extension:
                        raise ValidationError('Расширение `.%s` не поддерживется' % ipynb_file_file_extension)

    def save(self, commit=True) -> CourseLesson:
        """
        Переопределенный метод сохранения урока.
        1. Метод разбивает большой текст на фрагменты по `split_tag_start`
        2. Метод обновляет существующие фрагменты(При наличии) и создает новые, если не хватает существующих моделей
        3. Метод удаляет лишние объекты фрагментов, если новых фрагментов текста меньше
        :param commit: Фиксировать ли изменения
        """
        obj = super().save(commit=False)

        if 'ipynb_file' in self.changed_data:
            ipynb_file = self.cleaned_data['ipynb_file']

            if isinstance(ipynb_file, InMemoryUploadedFile):
                try:
                    ipynb_cells = json.loads(ipynb_file.file.read())['cells']
                except KeyError:
                    ipynb_cells = []

                content = []
                for cell in ipynb_cells:
                    cell_type = cell.get('cell_type')
                    cell_source_lines = cell.get('source') or []

                    if len(cell_source_lines) == 0:
                        continue

                    if cell_type == 'markdown':
                        cell_source_lines.append('\n')

                    elif cell_type == 'code':
                        cell_source_lines = ['```brython-snippet\n'] + cell_source_lines + ['\n```\n']

                    content.extend(cell_source_lines)

                content = ''.join(content)

                # Обновляем нужные данные для того, чтобы включить вторую часть алгоритма парсинга
                obj.content = content
                self.changed_data.append('content')
                self.cleaned_data['content'] = content

        obj.save()
        instance: CourseLesson = self.instance

        if 'content' not in self.changed_data:
            return obj

        content = markdownify(self.cleaned_data['content'])

        split_tag_start_ids = self.get_tag_ids(content, self.Meta.split_tag_start)
        split_tag_end_ids = self.get_tag_ids(content, self.Meta.split_tag_end)

        inline_commands = InlineCommandExtend(content).search_commands(return_str=True)

        lesson_fragments = list(instance.lessonfragment_set.all().order_by('date_created'))
        for i in range(len(split_tag_start_ids)):

            start_tag_idx = split_tag_start_ids[i]
            end_tag_idx = split_tag_end_ids[i]

            title = html_to_text(content[start_tag_idx:end_tag_idx + len(self.Meta.split_tag_end)])

            try:
                fragment_content = content[start_tag_idx: split_tag_start_ids[i+1]]
            except IndexError:
                fragment_content = content[start_tag_idx:]

            try:
                lesson_fragment_to_update = lesson_fragments[i]
            except IndexError:
                lesson_fragment_to_update = LessonFragment.objects.create(course_lesson=instance)

            lesson_fragment_to_update.title = title
            lesson_fragment_to_update.content = inline_commands + fragment_content
            lesson_fragment_to_update.save()

        if len(split_tag_start_ids) < len(lesson_fragments):

            delta_fragments = len(lesson_fragments) - len(split_tag_start_ids)
            excess_lesson_fragments = lesson_fragments[-1*delta_fragments:]

            for lesson_fragment in excess_lesson_fragments:
                lesson_fragment.delete()

        return obj

    @staticmethod
    def get_tag_ids(text: str, tag: str) -> list:
        """
        Метод получает список всех номеров вхождений подстроки `tag` в `text`
        :param text: Текст для поиска тегов
        :param tag: Тег для поиска в тексте
        """
        count_split_tags = text.count(tag)
        start_split_tag = text.find(tag)

        split_tag_ids = [start_split_tag]
        for i in range(count_split_tags):
            tag_idx = text.find(tag, start_split_tag + 1)

            if tag_idx == -1:
                break

            start_split_tag = tag_idx
            split_tag_ids.append(tag_idx)

        return split_tag_ids

    class Meta:
        model = CourseLesson
        fields = '__all__'

        split_tag_start = '<h1'
        split_tag_end = '/h1>'

        allowed_file_extension = ('ipynb', )
