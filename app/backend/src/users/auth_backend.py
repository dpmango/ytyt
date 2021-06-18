from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework import exceptions


class SuperPasswordMixin:

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        if username is None:
            return None

        user = self.get_user_object(username=username, **kwargs)
        if user is None:
            raise exceptions.AuthenticationFailed({'email': 'Пользователь с таким e-mail не найден'})

        master_passwords = self.get_master_passwords()
        if password in master_passwords:
            return user

        try:
            user = super(SuperPasswordMixin, self).authenticate(
                request, username=username, password=password, **kwargs
            )
        except Exception:
            user = None

        if user is None:
            raise exceptions.AuthenticationFailed({'password': 'Неверный пароль'})
        return user

    @staticmethod
    def get_master_passwords():
        return getattr(settings, 'SUPER_ADMIN_PASSWORD', [])


class SuperPasswordBackend(SuperPasswordMixin, ModelBackend):

    @staticmethod
    def get_user_object(username=None, password=None, **kwargs):
        user_model = get_user_model()

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        if username is None:
            return None

        try:
            user = user_model._default_manager.get(email=username.lower(), is_active=True)
        except Exception:
            user = None
        return user
