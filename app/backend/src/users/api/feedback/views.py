from django.contrib.auth.models import AnonymousUser
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.decorators import api_view, schema, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from providers.mailgun.mixins import EmailNotification
from users.api.feedback.serializers import UserFeedBackSerializers, AnonymousFeedBackSerializers


@api_view(['POST'])
@permission_classes([AllowAny])
@schema(AutoSchema())
def feedback(request):
    """
    Функция обрабатывает обратную связь от пользователя.
    Если пользователь авторизован:
        - Обязательными параметрами будут являться: phone
    Если пользователь не авторизован:
        - Обязательными параметрами будут являться: phone, first_name, email
    """

    if isinstance(request.user, AnonymousUser):
        serializer = AnonymousFeedBackSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject_template_raw = 'Запрос на звонок от незарегистрированного пользователя'
        context = serializer.validated_data

    else:
        serializer = UserFeedBackSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        subject_template_raw = 'Запрос на звонок от студента'
        context = {**model_to_dict(request.user), **serializer.validated_data}

    mailgun = EmailNotification(
        subject_template_raw=subject_template_raw,
        email_template_raw='Имя: {first_name}\nEmail: {email}\nНомер телефона: {phone}',
    )

    mailgun.send_mail(context)
    return Response(status=status.HTTP_204_NO_CONTENT)
