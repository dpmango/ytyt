from django.conf import settings
from django.template import loader

from providers.tasks import send_mail, send_file


class EmailNotificationMixin:
    """
    Класс-миксин для асинхрнного отправления сообщения на почту.
    Поддерживает темплейт для заголовка и тела
    """
    subject_template_raw = None
    email_template_raw = None

    subject_template_name = None
    email_template_name = None

    def send_mail(self, context: dict = None, to: str = None, files: list = None) -> None:
        """
        Метод производит формирование темы и тела сообщения.
        Если темплейта не существует, то метод будет искать захаркоженные темплейты
        После направляет сообщение на отправку
        Если адресат не указан, то отправка будет произведена на админскую почту
        :param context: Контекстыне данные
        :param to: Адресат
        :param files: Набор файлов
        """
        to = to if to is not None else settings.DEFAULT_ADMIN_EMAIL

        if self.subject_template_name:
            subject = loader.render_to_string(self.subject_template_name, context or {})
            subject = ''.join(subject.splitlines())
        else:
            subject = self.subject_template_raw.format(**(context or {}))

        if self.email_template_name:
            body = loader.render_to_string(self.email_template_name, context or {})
        else:
            body = self.email_template_raw.format(**(context or {}))

        if files is None:
            if settings.IS_PRODUCTION:
                send_mail.delay(to, subject, body)
            else:
                send_mail(to, subject, body)
        else:
            if settings.IS_PRODUCTION:
                send_file.delay(to, subject, body, files)
            else:
                send_file(to, subject, body, files)


class EmailNotification(EmailNotificationMixin):
    """
    Класс для простой отправки писем, не используя миксин модели
    """

    def __init__(self,
                 subject_template_raw: str = None,
                 email_template_raw: str = None,
                 subject_template_name: str = None,
                 email_template_name: str = None):
        self.subject_template_raw = subject_template_raw
        self.email_template_raw = email_template_raw
        self.subject_template_name = subject_template_name
        self.email_template_name = email_template_name
