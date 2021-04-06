from rest_framework import serializers

from courses.api.course_theme.serializers import DefaultCourseThemeSerializers
from courses.models import Course
from courses_access.common.serializers import AccessBaseSerializers


class DefaultCourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class DetailCourseSerializers(AccessBaseSerializers):
    course_themes = serializers.SerializerMethodField()

    def get_course_themes(self, obj: Course):
        """
        Метод вернет доступные темы по выбранному курсу
        :param obj: Объект курса
        """
        return DefaultCourseThemeSerializers(obj.coursetheme_set.all(), many=True, context=self.context).data

    class Meta:
        model = Course
        fields = '__all__'
