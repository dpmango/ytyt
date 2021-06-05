from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_auth.views import (
    UserDetailsView as UserDetailsViewBase,
    PasswordResetConfirmView,
    PasswordChangeView,
    LoginView
)
from rest_framework import exceptions
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from providers.mailgun.mixins import EmailNotificationMixin
from users.models import User
from users.serializers import PasswordResetSerializer

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class PasswordResetView(GenericAPIView, EmailNotificationMixin):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    subject_template_name = 'users/password/password_reset_subject.txt'
    email_template_name = 'users/password/password_reset_body.html'

    def post(self, request, *args, **kwargs):
        """
        Метод отправляет ссылку на указанный email для восстановления пароля
        Пример: https://example.com/auth/reset/confirm?token=al6051-1b6854c210eab8e327129a8d878b68b8&uid=MjY
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.send_mail(**serializer.save())
        email = serializer.validated_data.get('email')

        return Response(
            {"detail": f'Ссылка для восстановления пароля отправлена на {email}.'},
            status=status.HTTP_200_OK
        )


class UserDetailsView(UserDetailsViewBase):
    """
    Переопределенный класс для работы с юзером, который запрашивает новые данные из бд, а не кэшируемые
    """
    queryset = User.objects.all()

    def get_object(self):
        try:
            return self.queryset.get(pk=self.request.user.pk)
        except User.DoesNotExist:
            raise exceptions.NotFound('Такого пользователя не существует.')


class PasswordResetConfirmViewCustom(PasswordResetConfirmView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Пароль изменён на новый.'})


class PasswordChangeViewCustom(PasswordChangeView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Новый пароль сохранён.'})


class LoginViewCustom(LoginView):
    pass
