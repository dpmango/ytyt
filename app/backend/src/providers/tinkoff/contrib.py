import json

from loguru import logger
from requests import request, Response


class Tinkoff:

    STATUS_NEW = 'NEW'
    STATUS_FORM_SHOWED = 'FORM_SHOWED'
    STATUS_DEADLINE_EXPIRED = 'DEADLINE_EXPIRED'
    STATUS_CANCELED = 'CANCELED'
    STATUS_PREAUTHORIZING = 'PREAUTHORIZING'
    STATUS_AUTHORIZING = 'AUTHORIZING'
    STATUS_AUTHORIZED = 'AUTHORIZED'
    STATUS_AUTH_FAIL = 'AUTH_FAIL'
    STATUS_REJECTED = 'REJECTED'
    STATUS_3DS_CHECKING = '3DS_CHECKING'
    STATUS_3DS_CHECKED = '3DS_CHECKED'
    STATUS_REVERSING = 'REVERSING'
    STATUS_PARTIAL_REVERSED = 'PARTIAL_REVERSED'
    STATUS_REVERSED = 'REVERSED'
    STATUS_CONFIRMING = 'CONFIRMING'
    STATUS_CONFIRMED = 'CONFIRMED'
    STATUS_REFUNDING = 'REFUNDING'
    STATUS_PARTIAL_REFUNDED = 'PARTIAL_REFUNDED'
    STATUS_REFUNDED = 'REFUNDED'

    STATUSES = (
        (STATUS_NEW, 'Создан'),
        (STATUS_FORM_SHOWED, 'Платежная форма открыта покупателем'),
        (STATUS_DEADLINE_EXPIRED, 'Просрочен'),
        (STATUS_CANCELED, 'Отменен'),
        (STATUS_PREAUTHORIZING, 'Проверка платежных данных'),
        (STATUS_AUTHORIZING, 'Резервируется'),
        (STATUS_AUTHORIZED, 'Зарезервирован'),
        (STATUS_AUTH_FAIL, 'Не прошел авторизацию'),
        (STATUS_REJECTED, 'Отклонен'),
        (STATUS_3DS_CHECKING, 'Проверяется по протоколу 3-D Secure'),
        (STATUS_3DS_CHECKED, 'Проверен по протоколу 3-D Secure'),
        (STATUS_REVERSING, 'Резервирование отменяется'),
        (STATUS_PARTIAL_REVERSED, 'Резервирование отменено частично'),
        (STATUS_REVERSED, 'Резервирование отменено'),
        (STATUS_CONFIRMING, 'Подтверждается'),
        (STATUS_CONFIRMED, 'Подтвержден'),
        (STATUS_REFUNDING, 'Возвращается'),
        (STATUS_PARTIAL_REFUNDED, 'Возвращен частично'),
        (STATUS_REFUNDED, 'Возвращен полностью'),
    )

    def __init__(self):
        self.base_url = None
        self._auth = None

    def _call(self, method: str, url: str, **kwargs):
        """
        Вызов необходимого метода API из url
        :param method: Метод для запроса
        :param url: url api-метода
        :param kwargs: Аргументы для вызова
        """
        base_url = self.base_url.rstrip('/')
        url = '%s/%s' % (base_url, url)

        logger.debug('[tinkoff][request][method=%s] url=%s, kwargs=%s' % (method, url, str(kwargs)))
        response = request(method=method, url=url, auth=self._auth, **kwargs)

        if response.status_code in (200, 201, 202):
            return self._force_json(response)

        logger.info('[tinkoff][response][method=%s] url=%s, response=%s' % (method, url, str(response)))
        return {}

    @staticmethod
    def _force_json(response: Response):
        try:
            return response.json()
        except json.JSONDecodeError:
            return {}
