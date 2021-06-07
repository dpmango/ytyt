from .url import base_url, base_front_url


def base_custom_context() -> dict:
    return {
        **base_url(None), **base_front_url(None),
    }
