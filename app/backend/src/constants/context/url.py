from django.conf import settings


def base_url(request) -> dict:
    return {'base_url': settings.BASE_URL}


def base_front_url(request) -> dict:
    return {'base_front_url': settings.BASE_FRONT_URL}
