from rest_framework import serializers
from courses.models import LessonFragment


class DefaultCourseSearchSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.SerializerMethodField()
    course_lesson = serializers.CharField(source='course_lesson.title')
    course_theme = serializers.CharField(source='course_lesson.course_theme.title')

    def get_description(self, obj: LessonFragment):
        """
        Метод выделяет подстроки с совпадениями и возвращает контекст вокруг них
        """
        result = []
        description = obj.get_text_description().lower()
        query_text = self.context.get('query_text')

        for text in query_text:
            idx = description.find(text.lower())
            if idx != -1:
                result.append(description[idx:idx+10])
        return ', '.join(result)

    class Meta:
        fields = ('id', 'title', 'description', 'course_lesson', 'course_theme')
