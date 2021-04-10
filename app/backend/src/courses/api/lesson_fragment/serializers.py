from rest_framework import serializers
from courses.models import LessonFragment
from courses_access.common.serializers import AccessBaseSerializers


class DefaultLessonFragmentSerializers(AccessBaseSerializers):
    class Meta:
        model = LessonFragment
        fields = ('id', 'title', )


class DetailLessonFragmentSerializers(AccessBaseSerializers):
    content = serializers.SerializerMethodField()

    @staticmethod
    def get_content(obj: LessonFragment) -> str:
        return obj.get_content()

    class Meta:
        model = LessonFragment
        exclude = ('date_created', )
