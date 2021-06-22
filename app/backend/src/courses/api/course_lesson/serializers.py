from rest_framework import serializers

from courses.api.lesson_fragment.serializers import (
    DetailLessonFragmentSerializers, DefaultLessonFragmentSerializers
)
from courses.models import CourseLesson
from courses.models import LessonFragment
from courses_access.api.serializers import DetailAccessSerializer, DetailAccessWithThemeSerializer
from collections import defaultdict
from courses_access.common.serializers import AccessBaseSerializers
from courses_access.models import Access
from courses_access.utils.any_ import get_course_from_struct


class DefaultCourseLessonSerializers(AccessBaseSerializers):
    class Meta:
        model = CourseLesson
        exclude = ('content', 'order', 'date_updated', 'date_created', 'ipynb_file')


class CourseLessonInMessageSerializers(AccessBaseSerializers):
    class Meta:
        model = CourseLesson
        fields = ('id', 'course_theme_id', 'title', 'status')


class DetailCourseLessonSerializers(DefaultCourseLessonSerializers):
    lesson_fragments = DefaultLessonFragmentSerializers(source='lessonfragment_set', many=True)
    accessible_lesson_fragments = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()

    def get_accessible_lesson_fragments(self, obj: CourseLesson) -> list:
        """
        Метод вернет все доступные фрагменты курса для пользователя
        :param obj: CourseLesson
        """
        course_id = get_course_from_struct(obj)
        user = self.context.get('user')

        if user.in_stuff_groups:
            accessible_objects = obj.lessonfragment_set.values_list('pk', flat=True)

        else:
            access = Access.objects.filter(course_id=course_id, user=user).first()
            if not access:
                return []

            # Если сущетсвует доступ к уроку, то вернем все фрагменты
            if access.check_manual_access(obj.__class__.__name__, obj.pk):
                accessible_objects = obj.lessonfragment_set.values_list('pk', flat=True)
            else:
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
        fragments = obj.lessonfragment_set.count() or 1

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

    def get_meta(self, instance: CourseLesson):
        """
        Метод вернет дополнительную информацию по следующему/текущему/предыдущему фрагменту/уроку/теме
        {
            theme: {
                next: {
                    ...
                },
                current: {
                    ...
                },
                prev: {
                    ...
                }
            },
            lesson: {
                next: {
                    ...
                },
                current: {
                    ...
                },
                prev: {
                    ...
                }
            }
        }
        """
        user = self.context.get('user')
        course_theme = instance.course_theme

        course_id = course_theme.course_id
        theme_id = course_theme.id
        lesson_id = instance.id

        mapping = (
            ('course_theme', DetailAccessSerializer, theme_id),
            ('course_lesson', DetailAccessWithThemeSerializer, lesson_id),
        )

        access = Access.objects.filter(user=user, course_id=course_id).first()
        if not access:
            return None

        meta = defaultdict(dict)
        for struct, serializer, id_ in mapping:
            context = {
                **self.context, 'access': access, 'struct': struct, 'course_theme': course_theme,
            }

            meta[struct]['current'] = serializer(
                access.get_object(struct, id_), context=context).data

            meta[struct]['next'] = serializer(
                access.get_direction_obj(struct, id_, direction='next'), context=context).data

            meta[struct]['prev'] = serializer(
                access.get_direction_obj(struct, id_, direction='prev'), context=context).data

        return meta

    class Meta:
        model = CourseLesson
        exclude = ('content', 'order', 'date_updated', 'date_created')
