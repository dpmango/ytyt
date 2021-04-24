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

    GENERATING_NOTIFICATIONS_EVENTS = (
        EVENT_DIALOG_MESSAGES_CREATE, EVENT_DIALOG_MESSAGES_SEEN
    )

    @staticmethod
    def generate_meta(limit, offset, total) -> dict:
        """
        Получение метаданных ответа на событиях, где есть пагинация
        :param limit: Количество записей
        :param offset: Количество записей для пропуска
        :param total: Общее количество записей сущности
        """
        return {
            'meta': {
                'limit': limit,
                'offset': offset,
                'total': total
            }
        }

    def _dialogs_load(self, user: User, limit=None, offset=None, **kwargs) -> dict:
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

        context = {'user': user, 'base_url': kwargs.get('base_url')}
        dialogs = DialogWithLastMessageSerializers(dialogs, many=True, context=context).data

        dialogs_with_unread_message = []
        dialogs_without_unread_message = []

        for _dialog in dialogs:
            last_message = _dialog.get('last_message') or {}

            if last_message.get('user') or {}.get('id') != user.id or last_message.get('date_read') is not None:
                dialogs_without_unread_message.append(_dialog)
            else:
                dialogs_with_unread_message.append(_dialog)

        sorted_func = lambda dialog: (dialog.get('last_message') or {}).get('date_created') or '2222-01-01'

        dialogs_with_unread_message = sorted(dialogs_with_unread_message, key=sorted_func)
        dialogs_without_unread_message = sorted(dialogs_without_unread_message, key=sorted_func)

        dialogs = dialogs_with_unread_message + dialogs_without_unread_message
        dialogs_count = user.dialog_users_set.count()
        return {'data': dialogs, 'to': user, **self.generate_meta(limit, offset, dialogs_count)}

    def _dialogs_messages_load(
            self, user: User, dialog_id=None, limit=None, offset=None, **kwargs) -> typing.Optional[dict]:
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
            return {'to': user, 'data': 'Не указан `dialog_id`', 'exception': True}

        dialog = Dialog.objects.filter(id=dialog_id).first()
        if not dialog or user not in dialog.users.all():
            return {'to': user, 'data': 'Диалог не принадлежит пользователю', 'exception': True}

        messages = DialogMessage.objects.filter(dialog=dialog).order_by('-date_created')

        messages_count = messages.count()
        messages = messages[offset:offset+limit]

        messages = sorted(messages, key=lambda message: message.date_created)

        context = {'user': user, 'base_url': kwargs.get('base_url')}
        messages = DefaultDialogMessageSerializers(messages, many=True, context=context).data

        return {'data': messages, 'to': user, **self.generate_meta(limit, offset, messages_count)}

    @staticmethod
    def _dialogs_messages_seen(user: User, dialog_id=None, message_id=None, **kwargs) -> typing.Optional[dict]:
        """
        Метод делает сообщение прочитанным
        :param user: Пользователь, который загрузил чат
        :param dialog_id: ID диалога
        :param message_id: ID сообщения, которое должно быть прочитанным
        """
        if not message_id:
            return {'to': user, 'data': 'Не указан `message_id`', 'exception': True}

        dialog = Dialog.objects.filter(id=dialog_id).first()
        if not dialog or user not in dialog.users.all():
            return {'to': user, 'data': 'Диалог не принадлежит пользователю', 'exception': True}

        message = DialogMessage.objects.get(id=message_id)
        message.date_read = timezone.now()
        message.save(update_fields=['date_read'])

        context = {'user': user, 'base_url': kwargs.get('base_url')}
        message = DefaultDialogMessageSerializers(message, context=context).data
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
        dialog = Dialog.objects.filter(id=dialog_id).first()
        if not dialog or user not in dialog.users.all():
            return {'to': user, 'data': 'Диалог не принадлежит пользователю', 'exception': True}

        if isinstance(file_id, int):
            file = File.objects.filter(id=file_id).first()
            if file.user != user:
                return {'to': user, 'data': 'Файл не принадлежит пользователю', 'exception': True}

        message = DialogMessage.objects.create(dialog_id=dialog_id, user=user, body=body, file_id=file_id)

        context = {'user': user, 'base_url': kwargs.get('base_url')}
        message = DefaultDialogMessageSerializers(message, context=context).data

        users_to_notification = set(dialog.users.all())
        users_to_email_notification = users_to_notification - {user}

        context = {**message, **model_to_dict(user)}

        for _user in users_to_email_notification:
            if _user.email_notifications:
                self.send_mail(context, _user.email)

        return {'data': message, 'to': users_to_notification}

    subject_template_raw = 'Новое сообщение от {email}'
    email_template_raw = 'Сообщение: {body}'
