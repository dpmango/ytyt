from rest_framework import serializers

from courses.models import CourseTheme
from courses_access.models import CourseThemeAccess


class DefaultCourseThemeSerializers(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj: CourseTheme):
        try:
            obj.coursethemeaccess_set.get(user=self.context.get('user')).status

        except CourseThemeAccess.DoesNotExist:
            return CourseThemeAccess.COURSES_STATUS_BLOCK

    class Meta:
        model = CourseTheme
        exclude = ('course', 'free_access')
