from django.db.models import Q

from users.models import User
from dialogs.models import DialogMessage


class InsidePlatformNotificationEvent:
    EVENT_NOTIFICATIONS_DIALOG_COUNT = 'notifications.dialogs.count'

    EVENTS = (
        (EVENT_NOTIFICATIONS_DIALOG_COUNT, 'Уведомление о количестве непрочитанных диалогов')
    )

    def get_dialogs_count(self, user) -> dict:
        """
        Функция для явного вызова события notifications.dialogs.count
        :param user: Пользователь
        """
        return {
            'data': self._notifications_dialogs_count(user),
            'event': self.EVENT_NOTIFICATIONS_DIALOG_COUNT,
        }

    @staticmethod
    def _notifications_dialogs_count(user: User, **kwargs) -> dict:
        """
        Метод подсччитывает количество диалогов, в которых есть непрочтенные сообщения
        :param user: Пользователь, для кого нужно посчитать непрочитанные диалоги
        :param kwargs: Возможные дополнительные аргументы
        """
        dialogs_count = DialogMessage.objects.filter(~Q(user=user), date_read__isnull=True).select_related('dialog')
        dialogs_count = dialogs_count.order_by('dialog__id').distinct('dialog__id').count()

        return {'data': dialogs_count, 'to': user}

    @classmethod
    def __name__(cls) -> str:
        return 'notifications'
