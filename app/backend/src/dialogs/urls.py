from django.urls import path
from dialogs.views import index, dialog


app_name = 'dialog'
urlpatterns = [
    path('', index, name='index'),
    path('<str:dialog_id>/', dialog, name='dialog'),
]
