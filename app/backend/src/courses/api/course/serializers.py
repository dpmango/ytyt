from django.contrib.auth.models import AnonymousUser
from django.db.models import Count
from rest_framework import serializers

from courses.models import Course
from courses_access.common.serializers import AccessSerializers
from courses_access.models import Access


class DefaultCourseSerializers(AccessSerializers):
    count_lessons = serializers.SerializerMethodField()
    completed_count_lessons = serializers.SerializerMethodField()

    count_themes = serializers.SerializerMethodField()
    completed_count_themes = serializers.SerializerMethodField()

    @staticmethod
    def get_count_lessons(obj: Course) -> int:
        """
        Метод возвращает общее количество урококов к курсу
        :param obj: Course
        """
        themes = obj.coursetheme_set.all()
        themes = themes.prefetch_related('courselesson_set')
        return themes.aggregate(cnt=Count('courselesson')).get('cnt')

    def get_completed_count_lessons(self, obj: Course) -> int:
        """
        Получение количества пройденных уроков курса
        :param obj: Объект курса
        """
        user = self.context.get('user')
        if not user or isinstance(user, AnonymousUser):
            return 0

        return Access.objects.count_by_status(to_struct='course_lesson', user_id=user.id)

    @staticmethod
    def get_count_themes(obj: Course) -> int:
        """
        Метод возвращает общее количество тем к курсу
        :param obj: Course
        """
        return obj.coursetheme_set.count()

    def get_completed_count_themes(self, obj: Course) -> int:
        """
        Метод возвращает количество завершенных тем курса
        :param obj: Объект курса
        """
        user = self.context.get('user')
        if not user or isinstance(user, AnonymousUser):
            return 0

        return Access.objects.count_by_status(
            to_struct='course_theme', user_id=user.id, course_id=obj.id
        )

    class Meta:
        model = Course
        exclude = ('order', 'date_created', 'date_updated')


class DetailCourseSerializers(AccessSerializers):

    def to_representation(self, instance: Course):
        user = self.context.get('user')
        access = Access.objects.filter(user=user, course_id=instance.id).first()

        if access and access.access_type == Access.STATUS_AVAILABLE:
            access.status = Access.STATUS_IN_PROGRESS
            access.save(update_fields=['status', 'date_updated'])

        return super().to_representation(instance)

    class Meta:
        model = Course
        exclude = ('order', 'date_created', 'date_updated')
