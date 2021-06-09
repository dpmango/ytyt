from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from courses_access.models import Access


class DetailAccessSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    status = serializers.SerializerMethodField()

    def get_status(self, obj) -> int:

        user = self.context.get('user')
        access = self.context.get('access')
        to_struct = self.context.get('struct')
        if user.in_stuff_groups:
            return Access.STATUS_AVAILABLE

        if not user or isinstance(user, AnonymousUser):
            return Access.STATUS_BLOCK

        target = access.get_object(to_struct, obj.pk)
        if target.status in Access.AVAILABLE_STATUSES:
            return target.status

        manual_access = access.check_manual_access(to_struct, obj.pk)
        if manual_access:
            return Access.STATUS_AVAILABLE

        theme = self.context.get('course_theme')
        if theme.free_access or access.access_type in Access.AVAILABLE_ACCESS_TYPES_FULL:

            if to_struct == 'course_theme':
                return Access.WAITING_STATUS_COMPLETED_THEME

            elif to_struct == 'course_lesson':
                return Access.WAITING_STATUS_COMPLETED_LESSON

            return Access.WAITING_STATUS_COMPLETED_FRAGMENT

        return Access.WAITING_STATUS_PAID


class DetailAccessWithThemeSerializer(DetailAccessSerializer):
    course_theme_id = serializers.IntegerField()
