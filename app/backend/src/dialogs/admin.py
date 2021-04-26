from django.contrib import admin
from dialogs.models import DialogMessage, Dialog


@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    pass


@admin.register(DialogMessage)
class DialogMessageAdmin(admin.ModelAdmin):
    pass

