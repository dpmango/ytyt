import typing as t
from collections import defaultdict

from django.utils import timezone

from dialogs.api.serializers import DialogWithLastMessageSerializers, DefaultDialogMessageWithReplySerializers
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
        messages = DefaultDialogMessageWithReplySerializers(messages, many=True, context=context).data

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
        if not dialog:
            return {'to': user, 'data': 'Диалог не указан', 'exception': True}

        dialog_users = dialog.users.all()
        if user not in dialog_users and not user.is_support:
            return {'to': user, 'data': 'Диалог не принадлежит пользователю', 'exception': True}

        message = DialogMessage.objects.get(id=message_id)
        message.date_read = timezone.now()
        message.save(update_fields=['date_read'])

        context = {'user': user, 'base_url': kwargs.get('base_url')}
        message = DefaultDialogMessageWithReplySerializers(message, context=context).data
        return {'data': message, 'to': dialog_users}

    def _dialogs_messages_create(
            self,
            user: User,
            dialog_id: int = None,
            body: str = None,
            file_id: int = None,
            lesson_id: int = None,
            reply_id: int = None,
            **kwargs
    ) -> t.Optional[dict]:
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
        if not dialog:
            return {'to': user, 'data': 'Диалог не указан', 'exception': True}

        dialog_users = dialog.users.all()
        if user not in dialog_users and not user.is_support:
            return {'to': user, 'data': 'Диалог не принадлежит пользователю', 'exception': True}

        file = None
        if isinstance(file_id, int):
            file = File.objects.filter(id=file_id).first()
            if file.user != user:
                return {'to': user, 'data': 'Файл не принадлежит пользователю', 'exception': True}

        if reply_id is not None:
            if not DialogMessage.objects.filter(id=reply_id, dialog_id=dialog_id).exists():
                return {'to': user, 'data': 'Сообщение не принадлежит диалогу', 'exception': True}

        message = DialogMessage.objects.create(
            dialog_id=dialog_id, user=user, body=body, file_id=file_id, lesson_id=lesson_id, reply_id=reply_id
        )

        context = {'user': user, 'base_url': kwargs.get('base_url')}
        message = DefaultDialogMessageWithReplySerializers(message, context=context).data
        mute = defaultdict(list)

        users_to_notification = set(dialog_users)
        users_to_email_notification = users_to_notification - {user}
        context = {'message': message, 'from': user}

        #  Если диалог с поддержкой, то уведомлять всех суппортов
        if dialog.with_support():
            supports = User.supports.all()
            users_to_notification |= set(supports)

            # Если отправитель суппорт, то обновлять количество непрочитанных сообщений у других суппортов не нужно
            if user.is_support:
                mute['notifications.dialogs.count'] = supports
                mute['notifications.dialogs.messages.count'] = supports

        if file is None:
            email_template_name = 'dialogs/message/index.html'
        else:
            if file.type == File.TYPE_IMAGE:
                email_template_name = 'dialogs/message-image/index.html'
                context = {**context, 'file_width': file.width, 'file_height': file.height}

            else:
                email_template_name = 'dialogs/message-file/index.html'

            context = {
                **context, 'file_url': file.generate_url(kwargs.get('base_url')), 'file_name': file.file_name
            }

        mailgun = EmailNotification(
            subject_template_raw='Новое сообщение от %s %s' % (user.first_name, user.last_name),
            email_template_name=email_template_name,
        )

        for user_ in users_to_email_notification:
            if user_.email_notifications:
                mailgun.send_mail(context={**context, 'email': user_.email}, to=user_.email)

        return {'data': message, 'to': users_to_notification, 'mute': mute}
