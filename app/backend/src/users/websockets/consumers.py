import json
import typing

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from loguru import logger

from users.models import User
from users.websockets.events.core import ConsumerEvents


class UserConsumer(JsonWebsocketConsumer, ConsumerEvents):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user: typing.Optional[User] = None

    def _declare(self) -> None:
        """
        Декларирование необходимых параметров для работы с сокетами
        """
        self.user = self.scope['user']

    def connect(self) -> None:
        """
        Подключение пользователя к сокету.
        """
        try:
            self._declare()
        except Exception as e:
            logger.warning('[ws] error=%s' % e)
            self.close(1000)
            return

        async_to_sync(self.channel_layer.group_add)(
            self.user.ws_key, self.channel_name
        )
        self.accept()

    def receive_json(self, content, **kwargs) -> None:
        """
        Метод обрабатывает все входящие сообщения от пользователя
        Метод распределяет входящий поток сообщений между нужными событиями
        :param content: Декодированные данные из сокета
        :param kwargs: Дополнительные аргументы
        """
        data = self.receive_event(content, user=self.user, **kwargs)
        self.push(user=self.user, data=data)

    def disconnect(self, close_code) -> None:
        """
        Отключение пользователя от диалога, если диалог существует
        :param close_code: Код отключения от сокета
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.user.ws_key, self.channel_name
        )

    def ws_send(self, event: dict) -> None:
        """
        Метод распределяет по всей подключенной группе
        :param event: Данные события
        """
        self.send(text_data=json.dumps(event))

    def push(self, user: User, data) -> None:
        async_to_sync(self.channel_layer.group_send)(
            user.ws_key, {'type': 'ws_send', **data}
        )
