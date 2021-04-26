import typing

from .dialogs import DialogEvent
from .notifications import InsidePlatformNotificationEvent
from .users import UserEvent


class ConsumerEvents:
    """
    Вспомогательный класс для поддержки событий в сокетах
    """

    _event_classes = {
        'users': UserEvent(),
        'dialogs': DialogEvent(),
        'notifications': InsidePlatformNotificationEvent(),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._declare_events()

    def _declare_events(self) -> None:
        """
        Декларирование всех существующих событий
        """
        self.events = type('Event', (), {event_name: event for event_name, event in self._event_classes.items()})()

    def get_generating_notifications_events(self) -> typing.List[str]:
        """
        Метод вернет список событий, которые должны порождать события уведомлений
        """
        return [
            event for event_obj in self._event_classes.values()
            for event in getattr(event_obj, 'GENERATING_NOTIFICATIONS_EVENTS', ())
        ]

    def get_name_events(self) -> typing.List[str]:
        """
        Получение всех возможных событий из каждого класса-события
        :return: Список с названиями событий
        """
        return [
            getattr(obj, event, None) for obj in self._event_classes.values() for event in obj.__dir__()
            if event.startswith('EVENT_')
        ]

    def receive_event(self, content: dict, **kwargs) -> dict:
        """
        Получение ответа от необходимого события сокета
        Если события нет в декларированных событиях, то исполнение метода закончится без ошибки
        :param content: Декодированные данные из сокекта
        :param kwargs: Дополнительные данные
        :return: Словарь с данные ответа от события
        """
        events = self.get_name_events()
        event: str = content.get('event')

        if event not in events:
            return {}

        event_class, *_ = event.split('.')
        event_func_name = '_%s' % event.replace('.', '_')

        event_obj = getattr(self.events, event_class, None)
        if not event_obj:
            return {}

        event_func = getattr(event_obj, event_func_name, None)
        if not event_func or not callable(event_func):
            return {}

        event_data = event_func(**content, **kwargs)
        if not isinstance(event_data, dict):
            return {}

        return {'event': event, **event_data}
