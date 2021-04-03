from rest_framework import serializers
from courses.models import CourseTheme


class DefaultCourseThemeSerializers(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        user = self.context.get('user')

        if user is None:
            return 


    class Meta:
        model = CourseTheme
        exclude = ('course', 'free_access')
