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
        event_data = self.receive_event(content, user=self.user, **kwargs)
        self.push(**event_data)

    def disconnect(self, close_code) -> None:
        """
        Отключение пользователя от диалога, если диалог существует
        :param close_code: Код отключения от сокета
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.user.ws_key, self.channel_name
        )

    def push(self, to: typing.Union[typing.Set[User], User], data: typing.Union[dict, list], **kwargs) -> None:
        """
        Непосредственная отправка данных в сокет.
        Момент отправки данных в сокет генерирует доплнительные события:
            - Уведолмения о количестве непрочитанных диалогов

        :param to: Набор пользователей, которым нужно разослать в сокет данные
        :param data: Данные для отправки
        """
        to = {to} if isinstance(to, User) else to

        for user in to:
            # Отправляем в сокет данные по основному событию
            async_to_sync(self.channel_layer.group_send)(user.ws_key, {'type': 'ws_send', 'data': data})

            if kwargs.get('event') in self.get_generating_notifications_events():

                # Порождаем дополнительные события для того же юзера
                async_to_sync(self.channel_layer.group_send)(
                    user.ws_key, {'type': 'ws_send', **self.events.notifications.get_dialogs_count(user)}
                )

    def ws_send(self, event: dict) -> None:
        """
        Метод распределяет по всей подключенной группе
        :param event: Данные события
        """
        self.send(text_data=json.dumps(event))
