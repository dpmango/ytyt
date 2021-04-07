from rest_framework import serializers

from courses.api.lesson_fragment.serializers import DefaultLessonFragmentSerializers
from courses.models import CourseLesson
from courses_access.common.serializers import AccessBaseSerializers
from courses_access.models.lesson_fragment import LessonFragmentAccess


class DefaultCourseLessonSerializers(AccessBaseSerializers):
    class Meta:
        model = CourseLesson
        exclude = ('description', )


class DetailCourseLessonSerializers(DefaultCourseLessonSerializers):
    count_lesson_fragments = serializers.SerializerMethodField()
    lesson_fragments = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    @staticmethod
    def get_description(obj: CourseLesson) -> str:
        return obj.get_description()

    def get_lesson_fragments(self, obj: CourseLesson) -> list:
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

        return DefaultLessonFragmentSerializers(access_fragments, many=True, context=self.context).data

    @staticmethod
    def get_count_lesson_fragments(obj: CourseLesson) -> int:
        """
        Метод возвращает общее количество фрагментов к уроку
        :param obj: CourseLesson
        """
        return obj.lessonfragment_set.count()

    class Meta:
        model = CourseLesson
        fields = '__all__'
