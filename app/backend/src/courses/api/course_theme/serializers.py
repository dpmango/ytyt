from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from courses.models import CourseTheme
from courses_access.common.serializers import AccessBaseSerializers
from courses_access.models import Access


class DefaultCourseThemeSerializers(AccessBaseSerializers):
    class Meta:
        model = CourseTheme
        exclude = ('course', 'free_access', 'order', 'date_updated', 'date_created')


class CourseThemeWithStatsSerializers(DefaultCourseThemeSerializers):
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

        access = Access.objects.filter(course=obj.course_id, user=user).first()
        if not access:
            return 0
        return access.count_by_status('course_lesson', _where=lambda item: item.course_theme_id == obj.pk)
