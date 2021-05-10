from rest_framework import serializers

from courses.api.lesson_fragment.serializers import (
    DetailLessonFragmentSerializers, DefaultLessonFragmentSerializers
)
from courses.models import CourseLesson
from courses.models import LessonFragment
from courses_access.common.serializers import AccessBaseSerializers
from courses_access.models import Access
from courses_access.utils import get_course_from_struct


class DefaultCourseLessonSerializers(AccessBaseSerializers):
    class Meta:
        model = CourseLesson
        exclude = ('content', 'order', 'course_theme', 'date_updated', 'date_created')


class DetailCourseLessonSerializers(DefaultCourseLessonSerializers):
    lesson_fragments = DefaultLessonFragmentSerializers(source='lessonfragment_set', many=True)
    accessible_lesson_fragments = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    def get_accessible_lesson_fragments(self, obj: CourseLesson) -> list:
        """
        Метод вернет все доступные фрагменты курса для пользователя
        :param obj: CourseLesson
        """
        course_id = get_course_from_struct(obj)
        user = self.context.get('user')

        access = Access.objects.filter(course_id=course_id, user=user).first()
        if not access:
            return []

        accessible_objects = access.get_accessible_objects(to_struct='lesson_fragment')
        accessible_objects = [item.pk for item in accessible_objects]

        access_fragments = LessonFragment.objects.filter(pk__in=accessible_objects, course_lesson=obj)
        return DetailLessonFragmentSerializers(access_fragments, many=True, context=self.context).data

    def get_progress(self, obj: CourseLesson) -> float:
        """
        Возвращает целочисленный процент прогресса пользователя по уроку
        :param obj: CourseLesson
        """
        user = self.context.get('user')
        fragments = obj.lessonfragment_set.count()

        course_id = get_course_from_struct(obj)
        access = Access.objects.filter(course=course_id, user=user).first()

        completed_fragments = 0
        if access:
            completed_fragments = access.count_by_status(
                'lesson_fragment', _where=lambda item: item.course_lesson_id == obj.pk
            )

        return completed_fragments / fragments * 100

    def to_representation(self, instance: CourseLesson):
        """
        Переопределенный метод сериализации объекта
        Метод дополнительно изменяет статус доступа к уроку и к теме на "В процессе", если он был "Доступен"
        :param instance: CourseLesson
        """
        user = self.context.get('user')
        course_id = get_course_from_struct(instance)
        access = Access.objects.filter(course_id=course_id, user=user).first()

        if access is not None:
            access.change_status(to_struct='course_lesson',
                                 pk=instance.pk,
                                 from_status=Access.STATUS_AVAILABLE,
                                 to_status=Access.STATUS_IN_PROGRESS)

            access.change_status(to_struct='course_theme',
                                 pk=instance.course_theme_id,
                                 from_status=Access.STATUS_AVAILABLE,
                                 to_status=Access.STATUS_IN_PROGRESS)

        return super().to_representation(instance)

    class Meta:
        model = CourseLesson
        exclude = ('content', 'order', 'date_updated', 'date_created')
