from rest_framework import serializers
from courses.models import Course


class DefaultCourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
