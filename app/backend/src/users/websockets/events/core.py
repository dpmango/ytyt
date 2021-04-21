import typing

from .dialogs import DialogEvent
from .notifications import InsidePlatformNotificationEvent


class ConsumerEvents(DialogEvent,
                     InsidePlatformNotificationEvent):
    """
    Вспомогательный класс для поддержки событий в сокетах
    """

    EVENT_DIALOG_LOAD = 'dialogs.load'
    EVENT_DIALOG_MESSAGES_LOAD = 'dialogs.messages.load'
    EVENT_DIALOG_MESSAGES_CREATE = 'dialogs.messages.create'
    EVENT_DIALOG_MESSAGES_SEEN = 'dialogs.messages.seen'

    EVENT_NOTIFICATIONS_DIALOG_COUNT = 'notifications.dialogs.count'

    EVENTS = (
        (EVENT_DIALOG_LOAD, 'Загрузка всех диалогов'),
        (EVENT_DIALOG_MESSAGES_LOAD, 'Загрузка сообщений диалога'),
        (EVENT_DIALOG_MESSAGES_CREATE, 'Создание сообщения в диалоге'),
        (EVENT_DIALOG_MESSAGES_SEEN, 'Сделать сообщение прочитанным')
    )

    def get_events(self) -> typing.List[str]:
        return list(map(lambda item: item[0], self.EVENTS))

    def receive_event(self, content: dict, **kwargs) -> dict:
        """
        Получение ответа от необходимого события сокета
        Если события нет в декларированных событиях, то исполнение метода закончится без ошибки
        :param content: Декодированные данные из сокекта
        :param kwargs: Дополнительные данные
        :return: Словарь с данные ответа от события
        """
        events = self.get_events()
        event: str = content.get('event')

        if event not in events:
            return {}

        event_func_name = '_%s' % event.replace('.', '_')
        event_func = getattr(self, event_func_name, None)
        if not event_func or not callable(event_func):
            return {}

        data = event_func(**content, **kwargs)
        return {'event': event, 'data': data}
