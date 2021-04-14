from rest_framework import serializers

from courses.models import LessonFragment
from courses_access.common.models import AccessBase
from courses_access.common.serializers import AccessBaseSerializers
from courses_access.models import LessonFragmentAccess


class DefaultLessonFragmentSerializers(AccessBaseSerializers):
    class Meta:
        model = LessonFragment
        fields = ('id', 'title', 'status')


class DetailLessonFragmentSerializers(AccessBaseSerializers):
    content = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    @staticmethod
    def get_content(obj: LessonFragment) -> str:
        return obj.get_content()

    def get_progress(self, obj: LessonFragment) -> float:
        """
        Возвращает целочисленный процент прогресса пользователя по уроку
        :param obj: LessonFragment
        """
        user = self.context.get('user')

        fragments = obj.course_lesson.lessonfragment_set.count()
        completed_fragments = LessonFragmentAccess.objects.filter(
            status=AccessBase.COURSES_STATUS_COMPLETED, lesson_fragment__course_lesson=obj.course_lesson, user=user,
        ).count()

        return completed_fragments / fragments * 100

    def to_representation(self, instance: LessonFragment):
        """
        Переопределенный метод сериализации объекта
        Метод дополнительно изменяет статус доступа к фрагменту на "В процессе", если он был доступен
        :param instance: LessonFragment
        """
        user = self.context.get('user')
        access_fragment = LessonFragmentAccess.objects.filter(lesson_fragment=instance, user=user).first()

        if access_fragment and access_fragment.status == AccessBase.COURSES_STATUS_AVAILABLE:
            access_fragment.status = AccessBase.COURSES_STATUS_IN_PROGRESS
            access_fragment.save(update_fields=['status'])

        return super().to_representation(instance)

    class Meta:
        model = LessonFragment
        exclude = ('date_created', 'date_updated')
