from providers.mailgun.contrib import mailgun



def send_mail(*args, **kwargs):
    mailgun.send_email(*args)
