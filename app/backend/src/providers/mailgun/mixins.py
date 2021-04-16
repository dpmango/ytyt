from django.template import loader
from providers.mailgun.contrib import mailgun


class EmailNotificationMixin:
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
        # TODO: когда появится Celery — вынести это туда
        mailgun.send_email(to, subject, body)
