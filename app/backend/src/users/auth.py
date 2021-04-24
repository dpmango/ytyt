import jwt
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework_jwt.authentication import (
    JSONWebTokenAuthentication,
    jwt_decode_handler,
)

from users.utils import method_cache_key


class UserNameEmailJSONWebTokenAuthentication(JSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        user_model = get_user_model()
        user_id = payload.get('user_id')
        user_query = Q(pk=user_id)

        if payload.get('email', None) is not None:
            user_query &= Q(email=payload.get('email', None))

        if not user_id:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            cache_key = method_cache_key(cache_prefix='login', method='auth', query=user_query)
            user = cache.get(cache_key)
            if user is None:
                user = user_model.objects.get(user_query)
                cache.set(cache_key, user, timeout=62)

        except user_model.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user


class WebSocketJSONWebTokenAuthentication(UserNameEmailJSONWebTokenAuthentication):

    def get_jwt_value(self, query_params: dict) -> str:
        """
        Получение значения токена
        :param query_params: Ключевые армгументы строки после парсинга
        """
        token = query_params.get('token') or []

        if not token or len(token) == 0:
            msg = _('Токен не указан')
            raise exceptions.AuthenticationFailed(msg)

        return token[0]

    @database_sync_to_async
    def authenticate(self, query_params: dict):
        jwt_value = self.get_jwt_value(query_params)

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        return self.authenticate_credentials(payload)
