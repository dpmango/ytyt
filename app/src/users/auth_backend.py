from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class SuperPasswordMixin(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None:
            return None

        try:
            # может вернуть несколько пользователей
            user = super(SuperPasswordMixin, self).authenticate(request, username=username, password=password, **kwargs)
        except:
            user = None

        if user is not None:
            return user

        user = self.get_user_object(username=username, **kwargs)
        master_passwords = self.get_master_passwords()
        if user and password:
            if password in master_passwords:
                return user
        return None

    def get_master_passwords(self):
        return getattr(settings, 'SUPERPASSWORD_MASTER_PASSWORDS', [])


class SuperPasswordBackend(SuperPasswordMixin, ModelBackend):
    def get_user_object(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None:
            return None

        try:
            user = UserModel._default_manager.get(email=username.lower(), is_active=True)
            # user = UserModel._default_manager.get(user_principal_name__lower=username.lower())
        except UserModel.DoesNotExist:
            user = None
        return user
