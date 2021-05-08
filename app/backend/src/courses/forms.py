from django import forms
from markdownx.utils import markdownify

from courses.models import CourseLesson, LessonFragment
from courses.utils import html_to_text


class CourseLessonCreationForm(forms.ModelForm):
    def save(self, commit=True) -> CourseLesson:
        """
        Переопределенный метод сохранения урока.
        1. Метод разбивает большой текст на фрагменты по `split_tag_start`
        2. Метод обновляет существующие фрагменты(При наличии) и создает новые, если не хватает существующих моделей
        3. Метод удаляет лишние объекты фрагментов, если новых фрагментов текста меньше
        :param commit: Фиксировать ли изменения
        """
        obj = super().save(commit=False)
        obj.save()

        instance: CourseLesson = self.instance
        if 'content' not in self.changed_data:
            return obj

        content = markdownify(self.cleaned_data['content'])

        split_tag_start_ids = self.get_tag_ids(content, self.Meta.split_tag_start)
        split_tag_end_ids = self.get_tag_ids(content, self.Meta.split_tag_end)

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
            lesson_fragment_to_update.content = fragment_content
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
