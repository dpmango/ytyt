import json
import typing as t

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings
from loguru import logger

from users.models import User
from users.websockets.events.core import ConsumerEvents


class UserConsumer(JsonWebsocketConsumer, ConsumerEvents):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user: t.Optional[User] = None
        self.base_url = settings.BASE_URL

    def _declare(self) -> None:
        """
        Декларирование необходимых параметров для работы с сокетами
        """
        self.user = self.scope['user']
        self.headers = {k.decode(): v.decode() for k, v in self.scope['headers']}

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
             to: t.Union[t.Set[User], User] = None,
             data: t.Union[dict, list] = None,
             mute: dict = None,
             **kwargs) -> None:
        """
        Непосредственная отправка данных в сокет.
        Момент отправки данных в сокет генерирует доплнительные события:
            - Уведолмения о количестве непрочитанных диалогов

        Дополнительно закрываем сокет, если данные для отправления и пользователь не существуют по какой-то причине
        :param to: Набор пользователей, которым нужно разослать в сокет данные
        :param mute: Структура с информацией о том, какие события и для каких пользователей мьютить
        :param data: Данные для отправки
        """
        content = kwargs.pop('content', None) or {}

        if to == data is None:
            self.close(1000)
            return

        # Если при обработке получили ошибку — отправляем ее в ответ и закрываем сокет
        elif kwargs.get('exception', False) is True:
            async_to_sync(self.channel_layer.group_send)(self.user.ws_key, {'type': 'ws_send', 'data': data, **kwargs})

        else:
            to = {to} if isinstance(to, User) else to
            mute = mute or {}
            for user in to:
                # Отправляем в сокет данные по основному событию
                async_to_sync(self.channel_layer.group_send)(user.ws_key, {'type': 'ws_send', 'data': data, **kwargs})

                if kwargs.get('event') not in self.get_generating_notifications_events():
                    continue

                # Порождаем дополнительное событие — количество диалогов с непрочитанными сообщениями
                # Если пользователь в мьюте для этого события, то ничего не нужно отправлять
                event_func = self.events.notifications.get_dialogs_count
                if user not in (mute.get(event_func.event_name) or set()):
                    async_to_sync(self.channel_layer.group_send)(
                        user.ws_key, {
                            'type': 'ws_send', **event_func(user)
                        }
                    )

                # Порождаем дополнительное событие — количество непрочитанных сообщений для каждого диалога
                event_func = self.events.notifications.get_dialog_messages_count
                if user not in (mute.get(event_func.event_name) or set()):
                    async_to_sync(self.channel_layer.group_send)(
                        user.ws_key, {
                            'type': 'ws_send', **event_func(user, **content)
                        }
                    )

    def ws_send(self, event: dict) -> None:
        """
        Метод распределяет по всей подключенной группе
        :param event: Данные события
        """
        self.send(text_data=json.dumps(event))
