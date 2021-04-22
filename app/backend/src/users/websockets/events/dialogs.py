import typing

from django.utils import timezone

from dialogs.api.serializers import DialogWithLastMessageSerializers, DefaultDialogMessageSerializers
from dialogs.models import DialogMessage, Dialog
from files.models import File
from providers.mailgun.mixins import EmailNotificationMixin
from users.models import User
from django.forms.models import model_to_dict


class DialogEvent(EmailNotificationMixin):
    EVENT_DIALOG_LOAD = 'dialogs.load'
    EVENT_DIALOG_MESSAGES_LOAD = 'dialogs.messages.load'
    EVENT_DIALOG_MESSAGES_CREATE = 'dialogs.messages.create'
    EVENT_DIALOG_MESSAGES_SEEN = 'dialogs.messages.seen'

    EVENTS = (
        (EVENT_DIALOG_LOAD, 'Загрузка всех диалогов'),
        (EVENT_DIALOG_MESSAGES_LOAD, 'Загрузка сообщений диалога'),
        (EVENT_DIALOG_MESSAGES_CREATE, 'Создание сообщения в диалоге'),
        (EVENT_DIALOG_MESSAGES_SEEN, 'Сделать сообщение прочитанным'),
    )

    @staticmethod
    def _dialogs_load(user: User, limit=None, offset=None, **kwargs) -> dict:
        """
        Получение всех диалогов пользователя
        :param user: Пользователь, который загрузил чат
        :param limit: Количество записей для выборки
        :param offset: Количество записей для пропуска
        """
        offset = offset or 0
        limit = limit or 20

        dialogs = user.dialog_users_set.all().order_by('id').prefetch_related('dialogmessage_set')
        dialogs = dialogs.distinct('id')[offset:limit]

        dialogs = DialogWithLastMessageSerializers(dialogs, many=True, context={'user': user}).data
        dialogs = sorted(
            dialogs, key=lambda dialog: (dialog.get('last_message') or {}).get('date_created') or '-1', reverse=True
        )
        return {'data': dialogs, 'to': user}

    @staticmethod
    def _dialogs_messages_load(user: User, dialog_id=None, limit=None, offset=None, **kwargs) -> typing.Optional[dict]:
        """
        Получение всех сообщений диалога
        :param user: Пользователь, который загрузил чат
        :param dialog_id: ID диалога
        :param limit: Количество записей для выборки
        :param offset: Количество записей для пропуска
        """
        offset = offset or 0
        limit = limit or 20

        if not dialog_id:
            return None

        dialog = Dialog.objects.filter(id=dialog_id).first()
        if not dialog or user not in dialog.users.all():
            return None

        messages = DialogMessage.objects.filter(dialog=dialog)[offset:limit]
        messages = DefaultDialogMessageSerializers(messages, many=True, context={'user': user}).data
        return {'data': messages, 'to': user}

    @staticmethod
    def _dialogs_messages_seen(user: User, dialog_id=None, message_id=None, **kwargs) -> typing.Optional[dict]:
        """
        Метод делает сообщение прочитанным
        :param user: Пользователь, который загрузил чат
        :param dialog_id: ID диалога
        :param message_id: ID сообщения, которое должно быть прочитанным
        """
        if not message_id:
            return None

        dialog = Dialog.objects.filter(id=dialog_id).first()
        if not dialog or user not in dialog.users.all():
            return None

        message = DialogMessage.objects.get(id=message_id)
        message.date_read = timezone.now()
        message = message.save(update_fields=['date_read'])

        return {'data': message, 'to': user}

    def _dialogs_messages_create(
            self, user: User, dialog_id=None, body=None, file_id=None, **kwargs) -> typing.Optional[dict]:
        """
        Создание сообщения
        Так же уведомляются все пользователи, которые есть в диалоге
        :param user: Пользователь, который загрузил чат
        :param dialog_id: ID диалога
        :param body: Тело сообщения
        :param file_id: ID файла
        :param kwargs: Дополнительные аргументы для создания сообщения
        :return: typing.Optional[dict]
        """
        if not dialog_id:
            return None

        dialog = Dialog.objects.filter(id=dialog_id).first()
        if not dialog or user not in dialog.users.all():
            return None

        if isinstance(file_id, int):
            file = File.objects.filter(id=file_id).first()
            if file.user != user:
                return None

        message = DialogMessage.objects.create(dialog_id=dialog_id, user=user, body=body, file_id=file_id)
        message = DefaultDialogMessageSerializers(message, context={'user': user}).data

        users_to_notification = set(dialog.users.all())
        users_to_email_notification = users_to_notification - {user}

        context = {**message, **model_to_dict(user)}

        for _user in users_to_email_notification:
            self.send_mail(context, _user.email)

        return {'data': message, 'to': users_to_notification}

    subject_template_raw = 'Новое сообщение от {email}'
    email_template_raw = 'Сообщение: {body}'
