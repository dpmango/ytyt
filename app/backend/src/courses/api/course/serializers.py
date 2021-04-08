from django.db.models import Count
from rest_framework import serializers

from courses.models import Course
from courses_access.common.serializers import AccessBaseSerializers


class DefaultCourseSerializers(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    count_themes = serializers.SerializerMethodField()

    @staticmethod
    def get_count_lessons(obj: Course) -> int:
        """
        Метод возвращает общее количество урококов к курсу
        :param obj: Course
        """
        themes = obj.coursetheme_set.all()
        themes = themes.prefetch_related('courselesson_set')
        return themes.aggregate(cnt=Count('courselesson')).get('cnt')

    @staticmethod
    def get_count_themes(obj: Course) -> int:
        """
        Метод возвращает общее количество тем к курсу
        :param obj: Course
        """
        return obj.coursetheme_set.count()

    class Meta:
        model = Course
        fields = '__all__'


class DetailCourseSerializers(AccessBaseSerializers):
    class Meta:
        model = Course
        fields = '__all__'
