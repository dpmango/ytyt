from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from courses_access.models import Access
from courses_access.utils import get_course_from_struct


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
        course_id = get_course_from_struct(obj)

        access = Access.objects.filter(course_id=course_id, user=user).first()

        if not user or isinstance(user, AnonymousUser) or not access:
            return Access.STATUS_BLOCK

        return access.get_status(obj.__class__.__name__, obj.pk)


class AccessSerializers(AccessBaseSerializers):
    course_access_type = serializers.SerializerMethodField()

    def get_course_access_type(self, obj) -> int:
        """
        Получение типа доступа к курсу при наличии пользователя
        :param obj: Объект Курса/Темы/Урока
        """
        user = self.context.get('user')
        if not user or isinstance(user, AnonymousUser):
            return Access.COURSE_ACCESS_TYPE_NONE

        course_id = get_course_from_struct(obj)
        access = Access.objects.filter(user=user, course_id=course_id).first()

        if access is None:
            return Access.COURSE_ACCESS_TYPE_NONE
        return access.access_type
