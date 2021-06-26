from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from django.db import transaction
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.http import urlsafe_base64_encode
from rest_auth import serializers as rest_auth_serializers
from rest_auth.registration import serializers as rest_auth_registration_serializers
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

from courses.models import Course
from files.utils import generate_thumb_url
from providers.tinkoff.contrib import Tinkoff
from providers.tinkoff_credit.contrib import TinkoffCredit
from users.models import User
from users.shortcuts import create_access_for_user
from users.tokens import token_generator


class UserDetailSerializer(serializers.ModelSerializer):
    thumbnail_avatar = serializers.SerializerMethodField()
    dialog = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    installment_available = serializers.SerializerMethodField()
    is_support = serializers.SerializerMethodField()

    @staticmethod
    def get_is_support(obj: User) -> bool:
        return obj.is_support

    @staticmethod
    def get_installment_available(obj: User) -> bool:
        """
        Метод вернет факт доступа к возможности оформления кредита
        :param obj: Объект пользователя
        """
        courses = Course.objects.all()
        return not any(
            course.paymentcredit_set.filter(user=obj, status=TinkoffCredit.STATUS_REJECTED).exists()
            for course in courses
        )

    @staticmethod
    def get_payment(obj: User) -> dict:
        result = {}
        courses = Course.objects.all()

        for course in courses:
            if course.payment_set.filter(user=obj, status=Tinkoff.STATUS_CONFIRMED).exists():
                result[str(course.pk)] = True

            elif course.paymentcredit_set.filter(user=obj, status=TinkoffCredit.STATUS_SIGNED).exists():
                result[str(course.pk)] = True

            else:
                result[str(course.pk)] = False

        return result

    @staticmethod
    def get_dialog(obj: User):
        """
        Получение диалога с ревьюером. Если запрашиваемый юзер — работник сервиса, то возвращать ничего не нужно
        :param obj: Пользователь
        """
        if obj.in_stuff_groups:
            return None

        dialog = obj.dialog_users_set.first()
        if not dialog:
            return None

        return {'id': dialog.id}

    def get_thumbnail_avatar(self, obj: User):
        if '/media/static' in obj.avatar.url:
            return None

        return generate_thumb_url(obj.avatar, settings.BASE_URL, '64x64')

    def to_representation(self, instance: User):
        data = super().to_representation(instance)

        if '/media/static' in instance.avatar.url:
            data['avatar'] = data['avatar'].replace('/media/static', '/static')
            data['thumbnail_avatar'] = data['avatar']

        return data

    @staticmethod
    def validate_repl_it_username(value: str) -> str:
        if not value.startswith('@'):
            raise ValidationError('Введите имя пользователя в формате @username')

        return value

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'repl_it_username',
            'avatar',
            'thumbnail_avatar',
            'email_notifications',
            'email_confirmed',
            'dialog',
            'payment',
            'installment_available',
            'is_support',
        )
        read_only_fields = ('email', 'id')


class UserDialogSmallDetailSerializer(UserDetailSerializer):
    status_online = serializers.SerializerMethodField()

    def get_thumbnail_avatar(self, obj: User):
        if '/media/static' in obj.avatar.url:
            return None

        return generate_thumb_url(obj.avatar, settings.BASE_URL, '64x64')

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
            'is_support',
        )


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        attrs['user'] = User.objects.filter(email=attrs.get('email')).first()

        if attrs['user'] is None:
            raise exceptions.NotFound({'detail': 'Пользователя с таким email не существует'})
        return attrs

    def save(self):
        user = self._validated_data['user']

        context = {
            'email': user.email,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
        }

        return {'to': user.email, 'context': context}


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        self.custom_validation(attrs)

        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(user=user, data=attrs)

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        if not token_generator.check_token(user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        return self.set_password_form.save()


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
        if not token or not token_generator.check_token(user, token):
            raise ValidationError({'token': ['Invalid value']})

        attrs['user'] = user
        return attrs

    def to_representation(self, instance: User):
        context = {
            'email': instance.email,
            'first_name': instance.first_name,
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            'token': token_generator.make_token(instance),
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
    first_name = serializers.CharField(required=True)
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
            4. Создан диалог с поддержкой
        :param request: Объект запроса
        """
        with transaction.atomic():
            user = super().save(request)
            create_access_for_user(user)

        return user
