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
    accessible_fragments = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    @staticmethod
    def get_description(obj: CourseLesson) -> str:
        return obj.get_description()

    def get_accessible_fragments(self, obj: CourseLesson):
        """
        Метод вернет все доступные фрагменты курса для пользователя
        :param obj: CourseLesson
        """
        access_fragments = LessonFragmentAccess.objects.filter(
            user=self.context.get('user'), lesson_fragment__course_lesson=obj
        )
        access_fragments = [f.lesson_fragment for f in access_fragments.select_related('lesson_fragment')]

        return DefaultLessonFragmentSerializers(access_fragments, many=True, context=self.context).data

    class Meta:
        model = CourseLesson
        fields = '__all__'
