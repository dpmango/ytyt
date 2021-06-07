from django.shortcuts import render
import uuid


def template_message(request):
    return render(
        request,
        'users/message/new_message_body.html', {
            'email': 'mat.coniaev2012@yandex.ru',
            'message': {
                'body': 'Hello world'
            },
            'from': type(
                'From', (), {
                    'first_name': 'Вася',
                    'last_name': 'Пупкин'
                }
            )(),
        }
    )


def template_password(request):
    return render(
        request,
        'users/password/password_reset_body.html', {
            'token': str(uuid.uuid4()),
            'uid': str(uuid.uuid4())[:7],
            'email': 'mat.coniaev2012@yandex.ru',
        }
    )


def template_verify_email(request):
    return render(
        request,
        'users/verify_email/verify_email_body.html', {
            'first_name': 'Matvey',
            'token': str(uuid.uuid4()),
            'uid': str(uuid.uuid4())[:7],
            'email': 'mat.coniaev2012@yandex.ru',
        }
    )
