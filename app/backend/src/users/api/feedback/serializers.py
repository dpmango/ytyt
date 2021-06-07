import re
from rest_framework import serializers


class UserFeedBackSerializers(serializers.Serializer):  # noqa
    phone = serializers.CharField(max_length=11, min_length=11, required=True)

    @staticmethod
    def validate_phone(value):
        if not re.fullmatch(r'79([0-9]{9})', value):
            raise serializers.ValidationError('Неверный формат телефона. Пример корректного формата: +79158765701')

        return value


class AnonymousFeedBackSerializers(UserFeedBackSerializers):  # noqa
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
