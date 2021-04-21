import typing

from django.utils import timezone

from dialogs.api.serializers import DialogWithLastMessageSerializers, DefaultDialogMessageSerializers
from dialogs.models import DialogMessage, Dialog
from files.models import File
from providers.mailgun.mixins import EmailNotificationMixin
from users.models import User


class DialogEvent(EmailNotificationMixin):

    @staticmethod
    def _dialogs_load(user: User, limit=None, offset=None, **kwargs) -> typing.Optional[list]:
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
        return sorted(
            dialogs, key=lambda dialog: (dialog.get('last_message') or {}).get('date_created') or '-1', reverse=True
        )

    @staticmethod
    def _dialogs_messages_load(user: User, dialog_id=None, limit=None, offset=None, **kwargs) -> typing.Optional[list]:
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
        return DefaultDialogMessageSerializers(messages, many=True, context={'user': user}).data

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
        message.save(update_fields=['date_read'])

        return DefaultDialogMessageSerializers(message, context={'user': user}).data

    def _dialogs_messages_create(self, user: User, dialog_id=None, body=None, file_id=None, **kwargs):
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

        # TODO: Если будут еще события, то вынести это в проверку доступов
        dialog = Dialog.objects.filter(id=dialog_id).first()
        if not dialog or user not in dialog.users.all():
            return None

        if isinstance(file_id, int):
            file = File.objects.filter(id=file_id).first()
            if file.user != user:
                return None

        message = DialogMessage.objects.create(dialog_id=dialog_id, user=user, body=body, file_id=file_id)
        message = DefaultDialogMessageSerializers(message, context={'user': user}).data

        users_to_notification = set(dialog.users.all()) - {user}

        for _user in users_to_notification:
            # self.send_mail(message, _user.email)
            self.push(data=message, user=_user)

        return message

    subject_template_raw = 'Новое сообщение от ...'
    email_template_raw = 'Сообщение: {body}'
