from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from courses.models import *
from courses_access.models import Access
from courses_access.utils.general import get_course_from_struct


class AccessBaseSerializers(serializers.ModelSerializer):
    """
    Базовый сериализатор для получения статуса доступа к модели из courses-app
    """
    status = serializers.SerializerMethodField()

    def get_status(self, obj) -> int:
        """
        Метод вернет информацию о доустпе к курсу
        Если пользователь ранее не имел доступ, то его необходимо запросить
        :param obj: Объект из courses-app
        """
        user = self.context.get('user')
        if user.in_stuff_groups:
            return Access.STATUS_AVAILABLE

        to_struct = obj.__class__.__name__
        course_id = get_course_from_struct(obj)

        access = Access.objects.filter(course_id=course_id, user=user).first()

        if not user or isinstance(user, AnonymousUser) or not access:
            return Access.STATUS_BLOCK

        if isinstance(obj, Course):
            return access.status

        target = access.get_object(to_struct, obj.pk)
        if target.status in Access.AVAILABLE_STATUSES:
            return target.status

        manual_access = access.check_manual_access(to_struct, obj.pk)
        if manual_access:
            return Access.STATUS_AVAILABLE

        theme = obj
        if isinstance(obj, CourseLesson):
            theme = obj.course_theme

        elif isinstance(obj, LessonFragment):
            theme = obj.course_lesson.course_theme

        if theme.free_access or access.access_type in Access.AVAILABLE_ACCESS_TYPES_FULL:

            if isinstance(obj, CourseTheme):
                return Access.WAITING_STATUS_COMPLETED_THEME

            elif isinstance(obj, CourseLesson):
                return Access.WAITING_STATUS_COMPLETED_LESSON

            return Access.WAITING_STATUS_COMPLETED_FRAGMENT

        return Access.WAITING_STATUS_PAID
