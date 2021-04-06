from courses.models import CourseTheme
from courses_access.common.serializers import AccessBaseSerializers


class DefaultCourseThemeSerializers(AccessBaseSerializers):
    class Meta:
        model = CourseTheme
        exclude = ('course', 'free_access')
