from django.contrib import admin
from dicts.models import Dicts


@admin.register(Dicts)
class DictsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')
