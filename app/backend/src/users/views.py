from django.shortcuts import render


def test_template(request):

    context = {
        'first_name': 'Матвей', 'last_name': 'Коняев', 'email': 'mat.coniaev2012@yandex.ru',
        'token': 'alkjshbdgvajsdhbjnahbsdjbjsaknh',
        'domain': 'localhost:8000',
        'protocol': 'http',
        'uid': 'KJHAD',
    }

    return render(request, 'users/verify_email/verify_email_body.html', context)

