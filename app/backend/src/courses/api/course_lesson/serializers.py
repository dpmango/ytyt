from rest_framework import serializers
from courses.models import CourseLesson, LessonFragment


class DefaultLessonFragmentSerializers(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    @staticmethod
    def get_description(obj: CourseLesson) -> str:
        return obj.get_description()

    class Meta:
        model = LessonFragment
        fields = '__all__'


class DefaultCourseLessonSerializers(serializers.ModelSerializer):
    count_fragments = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    @staticmethod
    def get_description(obj: CourseLesson) -> str:
        return obj.get_description()

    @staticmethod
    def get_count_fragments(obj: CourseLesson) -> int:
        return obj.lessonfragment_set.count()

    class Meta:
        model = CourseLesson
        fields = '__all__'


class DetailCourseLessonSerializers(DefaultCourseLessonSerializers):
    lesson_fragments = DefaultLessonFragmentSerializers(source='lessonfragment_set', many=True)

    class Meta:
        model = CourseLesson
        fields = '__all__'
