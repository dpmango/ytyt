from django.contrib.auth import get_user_model
from rest_auth import serializers as rest_auth_serializers
from rest_auth.registration import serializers as rest_auth_registration_serializers
from rest_framework import serializers

from users import permissions

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    # permissions = serializers.SerializerMethodField(read_only=True)
    group_id = serializers.IntegerField(source='get_group_id')
    group = serializers.CharField(source='get_group_title')

    # def get_permissions(self, obj):
    #     group_id = obj.get_group_id()
    #     result = []
    #     if group_id in permissions.GROUP_RIGHTS:
    #         result = permissions.GROUP_RIGHTS[group_id]
    #     return result

    class Meta:
        model = User
        fields = (
            'email', 'id', 'group_id', 'group', 'first_name', 'last_name', 'middle_name', 'phone', 'birthday', 'phone',
                  'gender',)
        read_only_fields = ('email', 'id',)


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
    pass
