from crm.celery import app
from providers.mailgun.contrib import mailgun


@app.task(bind=True)
def send_mail(_, *args, **kwargs) -> None:
    """
    Асинхронная отправка сообщений через mailgun
    :param _: Неиспользуемый объект celery
    :param args: Аргументы запроса
    :param kwargs: Ключевые аргументы запроса
    :return: None
    """
    mailgun.send_email(*args)


@app.task(bind=True)
def send_file(_, *args, **kwargs) -> None:
    """
    Асинхронная отправка сообщений через mailgun
    :param _: Неиспользуемый объект celery
    :param args: Аргументы запроса
    :param kwargs: Ключевые аргументы запроса
    :return: None
    """

    # https://documentation.mailgun.com/en/latest/user_manual.html#sending-via-api
    mailgun.send_file(*args)
