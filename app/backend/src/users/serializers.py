from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.http import urlsafe_base64_encode
from rest_auth import serializers as rest_auth_serializers
from rest_auth.registration import serializers as rest_auth_registration_serializers
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

from courses.models import Course
from courses_access.models.course import CourseAccess

from users.models import User


class UserDetailSerializer(serializers.ModelSerializer):

    def to_representation(self, instance: User):
        data = super().to_representation(instance)

        if '/media/static' in instance.avatar.url:
            data['avatar'] = data['avatar'].replace('/media/static', '/static')

        return data

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'github_url', 'avatar', 'email_notifications')
        read_only_fields = ('email', 'id')


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        attrs['user'] = User.objects.filter(email=attrs.get('email')).first()

        if attrs['user'] is None:
            raise exceptions.NotFound({'email': 'Пользователя с таким email не существует'})
        return attrs

    def save(self):
        user = self._validated_data['user']

        context = {
            'email': user.email,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'domain': self.context['domain'],
            'protocol': self.context['protocol'],
        }

        return {'to': user.email, 'context': context}


class VerifyEmailSerializer(serializers.Serializer):
    uid = serializers.CharField(required=False)
    token = serializers.CharField(required=False)

    def validate(self, attrs):

        try:
            uid = force_text(uid_decoder(attrs['uid']))
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        if not default_token_generator.check_token(user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        attrs['user'] = user
        return attrs

    def to_representation(self, instance: User):
        context = {
            'email': instance.email,
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            'user': instance,
            'token': default_token_generator.make_token(instance),
            'domain': self.context['domain'],
            'protocol': self.context['protocol'],
        }

        return {'to': instance.email, 'context': context}

    def save(self):
        user = self._validated_data['user']
        user.email_confirmed = True
        user.save(update_fields=['email_confirmed'])

        return user


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
