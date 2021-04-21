from django.shortcuts import render


def index(request):
    return render(request, 'dialogs/index.html')


def dialog(request, dialog_id):
    return render(request, 'dialogs/dialog.html', {'dialog_id': dialog_id})
