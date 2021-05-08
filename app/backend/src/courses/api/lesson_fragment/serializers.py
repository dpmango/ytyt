from rest_framework import serializers

from courses.models import LessonFragment
from courses_access.common.serializers import AccessBaseSerializers
from courses_access.models import Access
from courses_access.utils import get_course_from_struct


class DefaultLessonFragmentSerializers(AccessBaseSerializers):
    class Meta:
        model = LessonFragment
        fields = ('id', 'title', 'status')


class DetailLessonFragmentSerializers(AccessBaseSerializers):
    content = serializers.SerializerMethodField()

    @staticmethod
    def get_content(obj: LessonFragment) -> str:
        return obj.get_content()

    def to_representation(self, instance: LessonFragment):
        """
        Переопределенный метод сериализации объекта
        Метод дополнительно изменяет статус доступа к фрагменту на "В процессе", если он был доступен
        :param instance: LessonFragment
        """
        user = self.context.get('user')
        course_id = get_course_from_struct(instance)
        access = Access.objects.filter(user=user, course_id=course_id).first()

        if access is not None:
            access.change_status(to_struct=instance.__class__.__name__,
                                 pk=instance.pk,
                                 from_status=Access.STATUS_AVAILABLE,
                                 to_status=Access.STATUS_IN_PROGRESS)

        data = super().to_representation(instance)

        if self.context.get('set_progress'):
            data['progress'] = self.get_progress(instance)

        return data

    def get_progress(self, obj: LessonFragment) -> float:
        """
        Возвращает целочисленный процент прогресса пользователя по уроку
        :param obj: LessonFragment
        """
        user = self.context.get('user')

        fragments = obj.course_lesson.lessonfragment_set.count()

        course_id = get_course_from_struct(obj)
        access = Access.objects.filter(course=course_id, user=user).first()

        completed_fragments = 0
        if access:
            completed_fragments = access.count_by_status(
                'lesson_fragment', _where=lambda item: item.course_lesson_id == obj.course_lesson_id
            )

        return completed_fragments / fragments * 100

    class Meta:
        model = LessonFragment
        exclude = ('date_created', 'date_updated')
