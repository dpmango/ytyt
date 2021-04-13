from django.contrib.auth import get_user_model
from rest_auth import serializers as rest_auth_serializers
from rest_auth.registration import serializers as rest_auth_registration_serializers
from rest_framework import serializers

from courses.models import Course
from courses_access.models.course import CourseAccess

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):

    def to_representation(self, instance: User):

        if '/media/static' in instance.avatar.url:
            instance.avatar = instance.avatar.url.replace('/media/static', '/static')

        return super().to_representation(instance)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone',
            'first_name',
            'last_name',
            'middle_name',
            'birthday',
            'phone',
            'gender',
            'github_url',
            'avatar',
            'email_notifications',
        )
        read_only_fields = ('email', 'id', )


class PasswordResetSerializer(rest_auth_serializers.PasswordResetSerializer):

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        request = self.context.get('request')

        return {
            'domain_override': request.get_host()
        }


class PasswordChangeSerializer(rest_auth_serializers.PasswordChangeSerializer):

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Старый пароль неверный')
        return value


class RegisterSerializer(rest_auth_registration_serializers.RegisterSerializer):

    def save(self, request):
        user = super().save(request)

        # При регистрации юзера даем триал-доступ к курсу
        course = Course.objects.first()
        CourseAccess.objects.set_trial(course, user)

        return user
