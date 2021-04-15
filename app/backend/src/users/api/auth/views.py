from urllib.parse import urlparse

from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from providers.mailgun.mixins import EmailNotificationMixin
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
    email_template_name = 'users/password/password_reset_body.txt'

    def get_serializer_context(self):
        current_site = urlparse(self.request.build_absolute_uri(''))

        return {
            **super().get_serializer_context(),
            'domain': current_site.netloc,
            'protocol': current_site.scheme
        }

    def post(self, request, *args, **kwargs):
        """
        Метод отправляет ссылку на указанный email для восстановления пароля
        Пример: http://example.com/auth/reset/confirm?token=al6051-1b6854c210eab8e327129a8d878b68b8&uid=MjY
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.send_mail(**serializer.save())

        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )

