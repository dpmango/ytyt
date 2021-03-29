from rest_framework import serializers
from courses.models import CourseTheme


class DefaultCourseThemeSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseTheme
        exclude = ('course', )
