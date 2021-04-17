from django.template import loader
from providers.tasks import send_mail


class EmailNotificationMixin:
    """
    Класс-миксин для асинхрнного отправления сообщения на почту.
    Поддерживает темплейт для заголовка и тела
    """

    subject_template_name = None
    email_template_name = None

    def send_mail(self, context, to) -> None:
        """
        Метод производит формирование темы и тела сообщения.
        После направляет сообщение на отправку
        :param context: Контекстыне данные
        :param to: Адресат
        """
        subject = loader.render_to_string(self.subject_template_name, context)
        subject = ''.join(subject.splitlines())

        body = loader.render_to_string(self.email_template_name, context)
        send_mail.delay(to, subject, body)
