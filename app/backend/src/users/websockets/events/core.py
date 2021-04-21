import typing

from .dialogs import DialogEvent
from .notifications import InsidePlatformNotificationEvent


class ConsumerEvents:
    """
    Вспомогательный класс для поддержки событий в сокетах
    """

    _event_classes = (
        DialogEvent, InsidePlatformNotificationEvent
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._declare_events()

    def _declare_events(self) -> None:
        """
        Декларирование всех существующих событий
        """
        self.events = type('Event', (), {event.__name__(): event() for event in self._event_classes})

    def get_name_events(self) -> typing.List[str]:
        """
        Получение всех возможных событий из каждого класса-события
        :return: Список с названиями событий
        """
        return [
            getattr(cl, ev, None) for cl in self.events.__dir__() for ev in cl.__dir__() if ev.startswith('EVENT_')
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

        event_class, *_ = event.strip('.')
        event_func_name = '_%s' % event.replace('.', '_')
        event_func = getattr(self.events, event_func_name, None)

        if not event_func or not callable(event_func):
            return {}

        event_data = event_func(**content, **kwargs)
        if not isinstance(event_data, dict):
            return {}

        return {'event': event, **event_data}
