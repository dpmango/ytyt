from rest_framework import serializers

from courses.api.course_theme.serializers import DefaultCourseThemeSerializers
from courses.models import Course
from courses_access.models import CourseAccess


class DefaultCourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class DetailCourseSerializers(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    course_themes = serializers.SerializerMethodField()

    def get_status(self, obj: Course) -> bool:
        """
        Метод вернет информацию о доустпе к курсу
        Если пользователь ранее не имел доступ, то его необходимо запросить
        :param obj: Объект курса
        """
        try:
            return obj.courseaccess_set.get(user=self.context.get('user')).status
        except CourseAccess.DoesNotExist:
            return CourseAccess.COURSES_STATUS_BLOCK

    def get_course_themes(self, obj: Course):
        """
        Метод вернет доступные темы по выбранному курсу
        :param obj: Объект курса
        """
        return DefaultCourseThemeSerializers(obj.coursetheme_set.all(), many=True, context=self.context).data

    class Meta:
        model = Course
        fields = '__all__'
