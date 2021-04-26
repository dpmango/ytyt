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
        self.headers = {k.decode(): v.decode() for k, v in self.scope['headers']}
        self.base_url = self.headers.get('origin')

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

        async_to_sync(self.channel_layer.group_add)(self.user.ws_key, self.channel_name)
        User.objects.set_status_online(user_id=self.user.id)

        self.notification_related_users()
        self.accept()

    def notification_related_users(self) -> None:
        """
        Дополнительное уведомление всех связанных с пользователем людей
        """
        related_users = self.events.users.get_related_users(user=self.user)
        event_status_data = self.events.users.get_user_status_online(user=self.user)

        for _user in related_users:
            # Уведомляем о смене статуса пользователя
            async_to_sync(self.channel_layer.group_send)(_user.ws_key, {'type': 'ws_send', **event_status_data})

    def receive_json(self, content, **kwargs) -> None:
        """
        Метод обрабатывает все входящие сообщения от пользователя
        Метод распределяет входящий поток сообщений между нужными событиями
        :param content: Декодированные данные из сокета
        :param kwargs: Дополнительные аргументы
        """
        event_data = self.receive_event(content, user=self.user, base_url=self.base_url, **kwargs)
        self.push(**event_data, content=content)

    def disconnect(self, close_code) -> None:
        """
        Отключение пользователя от диалога, если диалог существует
        :param close_code: Код отключения от сокета
        """
        User.objects.set_status_offline(user_id=self.user.id)
        self.notification_related_users()

        async_to_sync(self.channel_layer.group_discard)(
            self.user.ws_key, self.channel_name
        )

    def push(self,
             to: typing.Union[typing.Set[User], User] = None, data: typing.Union[dict, list] = None, **kwargs) -> None:
        """
        Непосредственная отправка данных в сокет.
        Момент отправки данных в сокет генерирует доплнительные события:
            - Уведолмения о количестве непрочитанных диалогов

        Дополнительно закрываем сокет, если данные для отправления и пользователь не существуют по какой-то причине
        :param to: Набор пользователей, которым нужно разослать в сокет данные
        :param data: Данные для отправки
        """
        if to == data is None:
            self.close(1000)
            return

        # Если при обработке получили ошибку — отправляем ее в ответ и закрываем сокет
        elif kwargs.get('exception', False) is True:
            async_to_sync(self.channel_layer.group_send)(self.user.ws_key, {'type': 'ws_send', 'data': data, **kwargs})

        else:
            to = {to} if isinstance(to, User) else to
            for user in to:
                # Отправляем в сокет данные по основному событию
                async_to_sync(self.channel_layer.group_send)(user.ws_key, {'type': 'ws_send', 'data': data, **kwargs})

                if kwargs.get('event') in self.get_generating_notifications_events():

                    # Порождаем дополнительное событие — количество диалогов с непрочитанными сообщениями
                    async_to_sync(self.channel_layer.group_send)(
                        user.ws_key, {'type': 'ws_send', **self.events.notifications.get_dialogs_count(user)}
                    )

                    # Порождаем дополнительное событие — количество непрочитанных сообщений для каждого диалога
                    messages_count = self.events.notifications.get_dialog_messages_count(
                        user, **kwargs.get('content') or {}
                    )
                    async_to_sync(self.channel_layer.group_send)(user.ws_key, {'type': 'ws_send', **messages_count})

    def ws_send(self, event: dict) -> None:
        """
        Метод распределяет по всей подключенной группе
        :param event: Данные события
        """
        self.send(text_data=json.dumps(event))
