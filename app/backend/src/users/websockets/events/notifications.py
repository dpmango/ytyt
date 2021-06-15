from django.db.models import Q

from dialogs.models import Dialog, DialogMessage
from users.models import User
from users import permissions


class InsidePlatformNotificationEvent:
    EVENT_NOTIFICATIONS_DIALOG_COUNT = 'notifications.dialogs.count'
    EVENT_NOTIFICATIONS_DIALOG_MESSAGES_COUNT = 'notifications.dialogs.messages.count'

    EVENTS = (
        (EVENT_NOTIFICATIONS_DIALOG_COUNT, 'Уведомление о количестве непрочитанных диалогов'),
        (EVENT_NOTIFICATIONS_DIALOG_MESSAGES_COUNT, 'Уведомление о количестве непрочитанных сообщений в диалоге'),
    )

    def get_dialogs_count(self, user: User) -> dict:
        """
        Функция для явного вызова события notifications.dialogs.count
        :param user: Пользователь
        """
        data = self._notifications_dialogs_count(user)
        data = data.get('data')

        return {'data': data, 'event': self.EVENT_NOTIFICATIONS_DIALOG_COUNT}
    get_dialogs_count.event_name = EVENT_NOTIFICATIONS_DIALOG_COUNT

    @staticmethod
    def _notifications_dialogs_count(user: User, **kwargs) -> dict:
        """
        Метод подсчитывает количество диалогов, в которых есть непрочтенные сообщения
        :param user: Пользователь, для кого нужно посчитать непрочитанные диалоги
        :param kwargs: Возможные дополнительные аргументы
        """
        dialogs_count = []

        if user.is_support:
            dialogs = Dialog.objects.filter(with_role=permissions.GROUP_SUPPORT).prefetch_related('dialogmessage_set')
        else:
            dialogs = user.dialog_users_set.all().prefetch_related('dialogmessage_set')

        for dialog in dialogs:  # TODO: Переписать на sql-запрос

            query = ~Q(user=user) & Q(date_read__isnull=True)
            if user.is_support:
                query &= Q(user__is_staff=False)

            messages_count = dialog.dialogmessage_set.filter(query).count()
            messages_count = 1 if messages_count > 0 else 0
            dialogs_count.append(messages_count)

        return {'data': sum(dialogs_count), 'to': user}

    def get_dialog_messages_count(self, user: User, dialog_id=None, **kwargs) -> dict:
        """
        Функция для явного вызова события notifications.dialogs.messages.count
        :param user: Пользователь
        :param dialog_id: ID диалога для которого нужно посчитать количество непрочитанных сообщений
        """
        data = self._notifications_dialogs_messages_count(user, dialog_id=dialog_id)
        data = data.get('data')

        return {'data': data, 'event': self.EVENT_NOTIFICATIONS_DIALOG_MESSAGES_COUNT}
    get_dialog_messages_count.event_name = EVENT_NOTIFICATIONS_DIALOG_MESSAGES_COUNT

    @staticmethod
    def _notifications_dialogs_messages_count(user: User, dialog_id=None, **kwargs) -> dict:
        """
        Получение количества непрочитанных сообщений для диалога
        :param user: Пользователь
        :param dialog_id: ID диалога для которого нужно посчитать количество непрочитанных сообщений
        :param kwargs: Дополнительные аргументы
        """
        query = ~Q(user=user)
        if user.is_support:
            query &= ~Q(user__groups__in=[permissions.GROUP_SUPPORT])

        count = DialogMessage.objects.filter(query, date_read__isnull=True, dialog_id=dialog_id).count()
        return {'data': {'count': count, 'dialog_id': dialog_id}, 'to': user}
