from django.template import loader
from providers.tasks import send_mail
from django.conf import settings


class EmailNotificationMixin:
    """
    Класс-миксин для асинхрнного отправления сообщения на почту.
    Поддерживает темплейт для заголовка и тела
    """
    subject_template_raw = None
    email_template_raw = None

    subject_template_name = None
    email_template_name = None

    def send_mail(self, context: dict, to: str = None) -> None:
        """
        Метод производит формирование темы и тела сообщения.
        Если темплейта не существует, то метод будет искать захаркоженные темплейты
        После направляет сообщение на отправку
        Если адресат не указан, то отправка будет произведена на админскую почту
        :param context: Контекстыне данные
        :param to: Адресат
        """
        to = to if to is not None else settings.DEFAULT_ADMIN_EMAIL

        if self.subject_template_name:
            subject = loader.render_to_string(self.subject_template_name, context)
            subject = ''.join(subject.splitlines())
        else:
            subject = self.subject_template_raw.format(**context)

        if self.email_template_name:
            body = loader.render_to_string(self.email_template_name, context)
        else:
            body = self.email_template_raw.format(**context)

        send_mail.delay(to, subject, body)
