import typing as t
from collections import defaultdict

from django.utils import timezone

from dialogs.api.serializers import DialogWithLastMessageSerializers, DefaultDialogMessageSerializers
from dialogs.models import DialogMessage, Dialog
from files.models import File
from providers.mailgun.mixins import EmailNotification
from users import permissions
from users.models import User


class DialogEvent:
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

        if user.is_support:
            kw = dict(is_support=True, with_role=permissions.GROUP_SUPPORT, limit_=limit, offset_=offset)

            dialogs = Dialog.objects.order_by_last_unread_message(**kw)
            count = Dialog.objects.count_with_order_by(**kw)
        else:
            kw = dict(user_id_=user.id, limit_=limit, offset_=offset)

            dialogs = Dialog.objects.order_by_last_unread_message(**kw)
            count = Dialog.objects.count_with_order_by(**kw)

        context = {'user': user, 'base_url': kwargs.get('base_url')}
        dialogs = DialogWithLastMessageSerializers(dialogs, many=True, context=context).data

        return {'data': dialogs, 'to': user, **self.generate_meta(limit, offset, count)}

    def _dialogs_messages_load(self, user: User, dialog_id=None, limit=None, offset=None, **kwargs) -> t.Optional[dict]:
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
        if (not dialog or user not in dialog.users.all()) and not user.is_support:
            return {'to': user, 'data': 'Диалог не принадлежит пользователю', 'exception': True}

        messages = DialogMessage.objects.filter(dialog=dialog).order_by('-date_created')

        messages_count = messages.count()
        messages = messages[offset:offset+limit]

        messages = sorted(messages, key=lambda message: message.date_created)
        context = {'user': user, 'base_url': kwargs.get('base_url')}
        messages = DefaultDialogMessageSerializers(messages, many=True, context=context).data

        return {'data': messages, 'to': user, **self.generate_meta(limit, offset, messages_count)}

    @staticmethod
    def _dialogs_messages_seen(user: User, dialog_id=None, message_id=None, **kwargs) -> t.Optional[dict]:
        """
        Метод делает сообщение прочитанным
        :param user: Пользователь, который загрузил чат
        :param dialog_id: ID диалога
        :param message_id: ID сообщения, которое должно быть прочитанным
        """
        if not message_id:
            return {'to': user, 'data': 'Не указан `message_id`', 'exception': True}

        dialog = Dialog.objects.filter(id=dialog_id).first()
        dialog_users = dialog.users.all()
        if (not dialog or user not in dialog_users) and not user.is_support:
            return {'to': user, 'data': 'Диалог не принадлежит пользователю', 'exception': True}

        message = DialogMessage.objects.get(id=message_id)
        message.date_read = timezone.now()
        message.save(update_fields=['date_read'])

        context = {'user': user, 'base_url': kwargs.get('base_url')}
        message = DefaultDialogMessageSerializers(message, context=context).data
        return {'data': message, 'to': dialog_users}

    def _dialogs_messages_create(
            self, user: User, dialog_id=None, body=None, file_id=None, lesson_id=None, **kwargs) -> t.Optional[dict]:
        """
        Создание сообщения
        Так же уведомляются все пользователи, которые есть в диалоге
        :param user: Пользователь, который отправил сообщение
        :param dialog_id: ID диалога
        :param body: Тело сообщения
        :param file_id: ID файла
        :param lesson_id: ID урока, в котором задали вопрос
        :param kwargs: Дополнительные аргументы для создания сообщения
        :return: typing.Optional[dict]
        """
        dialog = Dialog.objects.filter(id=dialog_id).first()
        dialog_users = dialog.users.all()

        if (not dialog or user not in dialog_users) and not user.is_support:
            return {'to': user, 'data': 'Диалог не принадлежит пользователю', 'exception': True}

        file = None
        if isinstance(file_id, int):
            file = File.objects.filter(id=file_id).first()
            if file.user != user:
                return {'to': user, 'data': 'Файл не принадлежит пользователю', 'exception': True}

        message = DialogMessage.objects.create(
            dialog_id=dialog_id, user=user, body=body, file_id=file_id, lesson_id=lesson_id
        )

        context = {'user': user, 'base_url': kwargs.get('base_url')}
        message = DefaultDialogMessageSerializers(message, context=context).data
        mute = defaultdict(list)

        users_to_notification = set(dialog_users)
        users_to_email_notification = users_to_notification - {user}

        #  Если диалог с поддержкой, то уведомлять всех суппортов
        if dialog.with_support():
            supports = User.supports.all()
            users_to_notification |= set(supports)

            # Если отправитель суппорт, то обновлять количество непрочитанных сообщений у других суппортов не нужно
            if user.is_support:
                mute['notifications.dialogs.count'] = supports
                mute['notifications.dialogs.messages.count'] = supports

        email_to = list(users_to_email_notification)[0].email if len(users_to_email_notification) == 1 else 'None@admin'
        context = {'message': message, 'from': user, 'email': email_to}

        if file is None:
            email_template_name = 'users/message/index.html'
        else:
            if file.is_image():
                email_template_name = 'users/message-image/index.html'
            else:
                email_template_name = 'users/message-file/index.html'

            context = {
                **context, 'file_url': file.url(kwargs.get('base_url')), 'file_name': file.file_name
            }

        mailgun = EmailNotification(
            subject_template_raw='Новое сообщение от %s' % user.email,
            email_template_name=email_template_name
        )

        for _user in users_to_email_notification:
            if _user.email_notifications:
                mailgun.send_mail(context, _user.email)

        return {'data': message, 'to': users_to_notification, 'mute': mute}

