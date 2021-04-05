from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings


def method_cache_key(cache_prefix='cache', method='unknown', **kwargs):
    # не использовать inspect.stack()[1][3] – это очень медленно!
    sign_string = [cache_prefix, method]
    for k, v in dict(kwargs).items():
        sign_string.append('%s__%s' % (k, v))
    return '@'.join(sign_string)


jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


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