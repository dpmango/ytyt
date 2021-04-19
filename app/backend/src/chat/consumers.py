import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from users.models import User
from chat.models import Dialog, DialogMessage
from channels.db import database_sync_to_async
import typing
from chat.exceptions import DialogError
from users.models import User


class ChatConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user: typing.Optional[User] = None
        self.dialog: typing.Optional[Dialog] = None

    @staticmethod
    def get_dialog(dialog_id) -> Dialog:
        """
        Получение диалога по id
        Если диалога не существует, то отключаем юзера
        :param dialog_id: ID диалога
        """
        try:
            return Dialog.objects.get(id=dialog_id)
        except (Dialog.DoesNotExist, ValueError):
            raise DialogError

    def _declare(self) -> None:
        """
        Декларирование необходимых параметров для работы с сокетами
        """
        dialog_id = self.scope['url_route']['kwargs']['dialog_id']

        self.dialog = self.get_dialog(dialog_id)
        self.user = self.scope['user']

    def connect(self) -> None:
        """
        Подключение пользователя к сокету
        Метод выполняет декларирование всех необходимых переменных для дальнейшей работы и принимает коннект
        """

        try:
            self._declare()
        except DialogError:
            self.close()
            return

        async_to_sync(self.channel_layer.group_add)(
            self.dialog.websocket_key, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code) -> None:
        """
        Отключение пользователя от диалога, если диалог существует
        :param close_code: Код отключения от сокета
        """
        if self.dialog is None:
            return

        async_to_sync(self.channel_layer.group_discard)(
            self.dialog.websocket_key,
            self.channel_name
        )

    def receive_json(self, content, **kwargs):

        print(content)

        async_to_sync(self.channel_layer.group_send)(
            self.dialog.websocket_key,
            {
                'type': 'chat_message',
                'message': 'abc'
            }
        )



    # # Receive message from WebSocket
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #
    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))