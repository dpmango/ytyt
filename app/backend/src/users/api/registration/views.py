from urllib.parse import urlparse

from allauth.account import app_settings as allauth_settings
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_auth.app_settings import TokenSerializer, JWTSerializer
from rest_auth.registration.views import RegisterView as RegisterViewBase
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from providers.mailgun.mixins import EmailNotificationMixin
from users.serializers import VerifyEmailSerializer
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema


class RegisterView(RegisterViewBase):
    """
    Переопределенная вьюха для создания пользователя.
    Нужна для того, чтобы в сериализатор пробросить контекст
    """
    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent.")}

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': user,
                'token': self.token
            }
            return JWTSerializer(data, context=self.get_serializer_context()).data
        else:
            return TokenSerializer(user.auth_token).data


class VerifyEmailView(RetrieveAPIView, CreateAPIView, EmailNotificationMixin):
    """
    Класс для подтверждения email авторизованного пользователя
    """

    serializer_class = VerifyEmailSerializer
    permission_classes = (IsAuthenticated, )

    subject_template_name = 'users/verify_email/verify_email_subject.txt'
    email_template_name = 'users/verify_email/verify_email_body.txt'

    def post(self, request, *args, **kwargs):
        """
        Метод отправит пользователю ссылку для подтверждения email
        Пример: http://example.com/auth/verify-email/confirm?token=al6051-1b6854c210eab8e327129a8d878b68b8&uid=MjY
        """
        serializer = self.get_serializer(request.user)
        self.send_mail(**serializer.data)

        data = {'detail': 'Письмо для подтверждения email выслано'}
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[
        Parameter('uid', IN_QUERY, type=TYPE_STRING), Parameter('token', IN_QUERY, type=TYPE_STRING)])
    def get(self, request, *args, **kwargs):
        """
        Метод подтверждает email пользователя, если токен и uid корректные
        """
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {'detail': 'Email подтвержден'}
        return Response(data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        current_site = urlparse(self.request.build_absolute_uri(''))

        return {
            **super().get_serializer_context(),
            'domain': current_site.netloc,
            'protocol': current_site.scheme
        }