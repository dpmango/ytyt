from rest_framework import serializers
from courses_access.models import CourseAccess, CourseThemeAccess, CourseLessonAccess, LessonFragmentAccess
from courses.models import Course, CourseTheme, CourseLesson


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


class AccessSerializers(AccessBaseSerializers):
    course_access_type = serializers.SerializerMethodField()

    def get_course_access_type(self, obj) -> int:

        user = self.context.get('user')
        course_id = None

        if isinstance(obj, Course):
            course_id = obj.id

        elif isinstance(obj, CourseTheme):
            course_id = obj.course_id

        elif isinstance(obj, CourseLesson):
            course_id = obj.course_theme.course_id

        course_access = CourseAccess.objects.filter(user=user, course_id=course_id).first()

        if course_access is None:
            return CourseAccess.COURSE_ACCESS_TYPE_NONE
        return course_access.access_type
