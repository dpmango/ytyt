from rest_framework import serializers

from courses.api.lesson_fragment.serializers import (
    DetailLessonFragmentSerializers, DefaultLessonFragmentSerializers
)
from courses.models import CourseLesson
from courses_access.common.models import AccessBase
from courses_access.common.serializers import AccessBaseSerializers
from courses_access.models.lesson_fragment import LessonFragmentAccess


class DefaultCourseLessonSerializers(AccessBaseSerializers):
    class Meta:
        model = CourseLesson
        exclude = ('content', 'order', 'course_theme')


class DetailCourseLessonSerializers(DefaultCourseLessonSerializers):
    lesson_fragments = DefaultLessonFragmentSerializers(source='lessonfragment_set', many=True)
    accessible_lesson_fragments = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    def get_accessible_lesson_fragments(self, obj: CourseLesson) -> list:
        """
        Метод вернет все доступные фрагменты курса для пользователя
        :param obj: CourseLesson
        """
        access_fragments = LessonFragmentAccess.objects.filter(
            lesson_fragment__course_lesson=obj, user=self.context.get('user')
        )
        access_fragments = access_fragments.distinct('lesson_fragment__id').order_by('lesson_fragment__id')
        access_fragments = access_fragments.select_related('lesson_fragment')
        access_fragments = [f.lesson_fragment for f in access_fragments]

        return DetailLessonFragmentSerializers(access_fragments, many=True, context=self.context).data

    def get_progress(self, obj: CourseLesson) -> float:
        """
        Возвращает целочисленный процент прогресса пользователя по уроку
        :param obj: CourseLesson
        """
        user = self.context.get('user')

        fragments = obj.lessonfragment_set.count()
        completed_fragments = LessonFragmentAccess.objects.filter(
            status=AccessBase.COURSES_STATUS_COMPLETED, lesson_fragment__course_lesson=obj, user=user,
        ).count()

        return completed_fragments / fragments * 100

    class Meta:
        model = CourseLesson
        exclude = ('content', 'order')
