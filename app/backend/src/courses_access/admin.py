from django.contrib import admin
from courses_access.models import Access


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    pass
