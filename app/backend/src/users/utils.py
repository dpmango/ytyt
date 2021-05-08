import json
from loguru import logger
from django.core.serializers.json import DjangoJSONEncoder


def method_cache_key(cache_prefix='cache', method='unknown', **kwargs):
    # не использовать inspect.stack()[1][3] – это очень медленно!
    sign_string = [cache_prefix, method]
    for k, v in dict(kwargs).items():
        sign_string.append('%s__%s' % (k, v))
    return '@'.join(sign_string)


def log_json_kwargs(event: str, **kwargs):
    data = kwargs
    logger.debug(
        '[%s], data_keys=%s, data_value:\n%s' % (
            event, kwargs.keys(), json.dumps(data, ensure_ascii=False, indent=4, cls=DjangoJSONEncoder)
        )
    )
