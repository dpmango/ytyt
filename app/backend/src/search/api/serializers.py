from rest_framework import serializers

from courses.api.course_lesson.serializers import DefaultCourseLessonSerializers
from courses.api.course_theme.serializers import DefaultCourseThemeSerializers


class DefaultCourseSearchSerializers(serializers.Serializer):
    course_title = serializers.CharField(source='course_lesson.course_theme.course.title')
    course_id = serializers.IntegerField(source='course_lesson.course_theme.course.id')
    course_theme = DefaultCourseThemeSerializers(source='course_lesson.course_theme')
    course_lesson = DefaultCourseLessonSerializers()

    class Meta:
        fields = '__all__'
