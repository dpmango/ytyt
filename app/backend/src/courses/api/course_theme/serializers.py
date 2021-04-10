from courses.models import CourseTheme
from courses_access.common.serializers import AccessSerializers


class DefaultCourseThemeSerializers(AccessSerializers):
    class Meta:
        model = CourseTheme
        exclude = ('course', 'free_access', 'order')
