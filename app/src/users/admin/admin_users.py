from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users.forms import UserCreationForm
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    add_form = UserCreationForm

    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'middle_name', 'gender', 'birthday', 'phone')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Courses Access'), {  # TODO: Обработатть добавление как в user_permissions
            'fields': ('user_access_course', 'user_access_course_block', 'user_access_course_block_lesson'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active',)}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)
