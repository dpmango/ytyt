from django.contrib import admin
from django.contrib.auth.models import Group


@admin.register(Group)
class UserAdmin(admin.ModelAdmin):
    pass
