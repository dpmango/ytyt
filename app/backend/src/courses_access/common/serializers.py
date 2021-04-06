from rest_framework import serializers
from courses_access.models import CourseAccess, CourseThemeAccess, CourseLessonAccess, LessonFragmentAccess


class AccessBaseSerializers(serializers.ModelSerializer):
    """
    Базовый сериализатор для получения статуса доступа к модели из courses-app
    """
    status = serializers.SerializerMethodField()

    MAPPING_ACCESS = {
        'CourseAccess': CourseAccess,
        'CourseThemeAccess': CourseThemeAccess,
        'CourseLessonAccess': CourseLessonAccess,
        'LessonFragmentAccess': LessonFragmentAccess,
    }

    def get_status(self, obj) -> int:
        """
        Метод вернет информацию о доустпе к курсу
        Если пользователь ранее не имел доступ, то его необходимо запросить
        :param obj: Объект из courses-app
        """
        return self.get_model_access(obj).objects.get_status(obj, user=self.context.get('user'))

    @classmethod
    def get_model_access(cls, obj):
        return cls.MAPPING_ACCESS.get(obj.__class__.__name__ + 'Access')
