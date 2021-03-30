from rest_framework import serializers
from courses.models import LessonFragment


class DefaultCourseSearchSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.SerializerMethodField()
    course_lesson = serializers.CharField(source='course_lesson.title')
    course_theme = serializers.CharField(source='course_lesson.course_theme.title')

    @staticmethod
    def get_description(obj: LessonFragment):
        """
        Метод выделяет подстроки с совпадениями и возвращает контекст вокруг них
        """
        return obj.course_lesson.get_text_description()

    class Meta:
        fields = ('id', 'title', 'description', 'course_lesson', 'course_theme')
