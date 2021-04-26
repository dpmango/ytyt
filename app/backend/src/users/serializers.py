from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.http import urlsafe_base64_encode
from rest_auth import serializers as rest_auth_serializers
from rest_auth.registration import serializers as rest_auth_registration_serializers
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from sorl.thumbnail import get_thumbnail

from courses.models import Course
from courses_access.models.course import CourseAccess
from dialogs.models import Dialog
from users.models import User


class UserDetailSerializer(serializers.ModelSerializer):
    thumbnail_avatar = serializers.SerializerMethodField()
    dialog = serializers.SerializerMethodField()

    @staticmethod
    def get_dialog(obj: User):
        """
        Получение диалога с ревьюером. Если запрашиваемый юзер — работник сервиса, то возвращать ничего не нужно
        :param obj: Пользователь
        """
        if obj.is_staff:
            return None

        dialog = obj.dialog_users_set.first()
        if not dialog:
            return None

        return {'id': dialog.id}

    def get_thumbnail_avatar(self, obj: User):
        if '/media/static' in obj.avatar.url:
            return None

        request = self.context.get('request')

        thumb = get_thumbnail(obj.avatar, '64x64', crop='center', quality=99)
        thumb_url = thumb.url

        return request.build_absolute_uri(urljoin(settings.MEDIA_URL, thumb_url))

    def to_representation(self, instance: User):
        data = super().to_representation(instance)

        if '/media/static' in instance.avatar.url:
            data['avatar'] = data['avatar'].replace('/media/static', '/static')
            data['thumbnail_avatar'] = data['avatar']

        return data

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'github_url',
            'avatar',
            'thumbnail_avatar',
            'email_notifications',
            'email_confirmed',
            'dialog'
        )
        read_only_fields = ('email', 'id')


class UserDialogSmallDetailSerializer(UserDetailSerializer):
    status_online = serializers.SerializerMethodField()

    def get_thumbnail_avatar(self, obj: User):
        if '/media/static' in obj.avatar.url:
            return None

        thumb = get_thumbnail(obj.avatar, '64x64', crop='center', quality=99)
        thumb_url = thumb.url

        return urljoin(settings.MEDIA_URL, thumb_url)

    def to_representation(self, instance: User):
        data = super().to_representation(instance)

        # Пробрасываем корректный base_url из сокета
        data['avatar'] = '/'.join([
            item.lstrip('/') for item in [self.context.get('base_url'), data['avatar']]
        ])
        data['thumbnail_avatar'] = '/'.join([
            item.lstrip('/') for item in [self.context.get('base_url'), data['thumbnail_avatar']]
        ])

        if '/media/static' in instance.avatar.url:
            data['avatar'] = data['avatar'].replace('/media/static', '/static')
            data['thumbnail_avatar'] = data['avatar']

        return data

    @staticmethod
    def get_status_online(obj: User):
        return User.objects.check_status_online(obj.id)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'thumbnail_avatar',
            'status_online',
        )


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
        except (TypeError, ValueError, OverflowError, KeyError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        token = attrs.get('token')
        if not token or not default_token_generator.check_token(user, token):
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
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def get_cleaned_data(self):
        return {
            **super().get_cleaned_data(),
            'first_name': self.validated_data.get('first_name') or '',
            'last_name': self.validated_data.get('last_name') or '',
        }

    def save(self, request) -> User:
        """
        Измененное поведение сохранение пользователя при регистрации
        Добавлено:
            1. Предоставление триал-версии к первому курсу
            2. Приставлен ревьюер-педагог
            3. Создан диалог с педагогом
        :param request: Объект запроса
        """
        user = super().save(request)

        course = Course.objects.order_by('id').first()
        if course:
            CourseAccess.objects.set_trial(course, user)

        educator = User.reviewers.get_less_busy_educator()
        user.reviewer = educator
        user.save()

        dialog = Dialog.objects.create()
        dialog.users.add(user, educator)
        dialog.save()

        return user
