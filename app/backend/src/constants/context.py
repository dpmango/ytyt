from django.conf import settings


def base_url(request) -> str:
    return settings.BASE_URL


def base_front_url(request) -> str:
    return settings.BASE_FRONT_URL
