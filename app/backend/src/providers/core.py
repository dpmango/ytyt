import json
from abc import ABC, abstractmethod

from loguru import logger
from requests import request, Response


class BaseProvider(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs):
        self.base_url: str = ...

    def _call(self, method: str, url: str, **kwargs):
        """
        Вызов необходимого метода API из url
        :param method: Метод для запроса
        :param url: url api-метода
        :param kwargs: Аргументы для вызова
        """
        base_url = self.base_url.rstrip('/')
        url = '%s/%s' % (base_url, url)

        logger.debug('[%s][request][method=%s] url=%s, kwargs=%s' % (
            self.__class__.__name__, method, url, str(kwargs)
        ))
        response = request(method=method, url=url, **kwargs, headers={'content-type': 'application/json'})

        if response.status_code in (200, 201, 202):
            return self._force_json(response)

        logger.info('[%s][response][method=%s] status_code=%s, url=%s, response=%s' % (
            self.__class__.__name__, method, response.status_code, url, str(response.text)
        ))

        response = self._force_json(response)
        if len(response) > 0:
            return {'error': response}

        return {}

    @staticmethod
    def is_error(data: dict):
        if 'error' in data:
            return data['error']

    @staticmethod
    def _force_json(response: Response):
        try:
            return response.json()
        except json.JSONDecodeError:
            return {}
