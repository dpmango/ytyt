import json
from typing import List, Tuple

from django.conf import settings
from loguru import logger
from requests import request, Response

from dicts.models import Dicts


class Mailgun:

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token

    @property
    def _auth(self):
        return 'api', self.token

    @property
    def from_email(self) -> str:
        return Dicts.defaults.from_email()

    def send_file(self, to: str, subject: str, files: List[Tuple[str, bytes]], **kwargs):
        """
        Метод отправляет сообщение пользователю на email
        :param to: Email пользователя
        :param subject: Тема сообщения
        :param files: Список файлов
        :param kwargs:
            - text: Текстовое сообщение
            - html: Сообщение в формате html
        """
        data = {'from': self.from_email, 'to': [to], 'subject': subject, **kwargs}
        return self._call('POST', url='messages', data=data, files=files)

    def send_email(self, to: str, subject: str, **kwargs) -> dict:
        """
        Метод отправляет сообщение пользователю на email
        :param to: Email пользователя
        :param subject: Тема сообщения
        :param kwargs:
            - text: Текстовое сообщение
            - html: Сообщение в формате html
        """
        data = {'from': self.from_email, 'to': [to], 'subject': subject, **kwargs}
        return self._call('POST', url='messages', data=data)

    def _call(self, method: str, url: str, **kwargs):
        """
        Вызов необходимого метода API из url
        :param method: Метод для запроса
        :param url: url api-метода
        :param kwargs: Аргументы для вызова
        """
        base_url = self.base_url.rstrip('/')
        url = '%s/%s' % (base_url, url)

        log_kwargs = kwargs
        if 'files' in log_kwargs:
            log_kwargs = {**log_kwargs, 'files': len(log_kwargs.get('files'))}

        if 'html' in log_kwargs.get('data') or {}:
            log_kwargs = {**log_kwargs, 'html': 'HTML-шаблон'}

        logger.debug('[mailgun][request][method=%s] url=%s, kwargs=%s' % (method, url, str(log_kwargs)))
        response = request(method=method, url=url, auth=self._auth, **kwargs)

        response = {
            'status_code': response.status_code,
            'data': self._force_json(response),
            'text': response.text,
        }

        logger.info('[mailgun][response][method=%s] url=%s, response=%s' % (method, url, str(response)))
        return response

    @staticmethod
    def _force_json(response: Response):
        try:
            return response.json()
        except json.JSONDecodeError:
            return {}


mailgun = Mailgun(
    base_url=settings.MAILGUN_HOST,
    token=settings.MAILGUN_TOKEN,
)
