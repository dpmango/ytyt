from rest_framework import serializers
from courses.models import LessonFragment
from courses_access.common.serializers import AccessBaseSerializers


class DefaultLessonFragmentSerializers(AccessBaseSerializers):
    description = serializers.SerializerMethodField()

    @staticmethod
    def get_description(obj: LessonFragment) -> str:
        return obj.get_description()

    class Meta:
        model = LessonFragment
        fields = '__all__'
