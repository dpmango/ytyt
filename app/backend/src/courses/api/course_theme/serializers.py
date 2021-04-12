from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from courses.models import CourseTheme
from courses_access.common.models import AccessBase
from courses_access.common.serializers import AccessSerializers
from courses_access.models import CourseLessonAccess


class DefaultCourseThemeSerializers(AccessSerializers):
    count_lessons = serializers.SerializerMethodField()
    completed_count_lessons = serializers.SerializerMethodField()

    @staticmethod
    def get_count_lessons(obj: CourseTheme) -> int:
        """
        Метод возвращает общее количество уроков к теме
        :param obj: CourseTheme
        """
        return obj.courselesson_set.count()

    def get_completed_count_lessons(self, obj: CourseTheme) -> int:
        """
        Получение количества пройденных уроков темы
        :param obj: CourseTheme
        """
        user = self.context.get('user')
        if not user or isinstance(user, AnonymousUser):
            return 0
        return CourseLessonAccess.objects.filter(
            user=user, course_lesson__course_theme=obj, status=AccessBase.COURSES_STATUS_COMPLETED
        ).count()

    class Meta:
        model = CourseTheme
        exclude = ('course', 'free_access', 'order')
