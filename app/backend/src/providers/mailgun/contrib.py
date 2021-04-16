import json

from requests import request, Response
from django.conf import settings


class Mailgun:

    def __init__(self, base_url: str, token: str, from_email: str):
        self.base_url = base_url
        self.token = token
        self.from_email = from_email

    @property
    def _auth(self):
        return 'api', self.token

    def send_email(self, to: str, subject: str, body: str) -> dict:
        """
        Метод отправляет сообщение пользователю на email
        :param to: Email пользователя
        :param subject: Тема сообщения
        :param body: Тело сообщения
        :return:
        """
        data = {
            'from': self.from_email, 'to': [to], 'subject': subject, 'text': body,
        }
        return self._call('POST', url='messages', data=data)

    def _call(self, method: str, url: str, **kwargs):
        """
        Вызов необходимого метода API из url
        :param method: Метод для запроса
        :param url: url api-метода
        :param kwargs: Аргументы для вызова
        """
        base_url = self.base_url.rstrip('/')
        response = request(method=method, url='%s/%s' % (base_url, url), auth=self._auth, **kwargs)

        return {
            'status_code': response.status_code,
            'data': self._force_json(response),
            'text': response.text,
        }

    @staticmethod
    def _force_json(response: Response):
        try:
            return response.json()
        except json.JSONDecodeError:
            return {}


mailgun = Mailgun(
    base_url=settings.MAILGUN_HOST,
    token=settings.MAILGUN_TOKEN,
    from_email=settings.DEFAULT_FROM_EMAIL,
)
