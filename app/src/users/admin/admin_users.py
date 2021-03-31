from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
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
            'fields': (
                'first_name',
                'last_name',
                'middle_name',
                'gender',
                'birthday',
                'phone',
                'get_avatar'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Courses Access'), {
            'fields': (
                'user_access_course',
                'user_access_course_theme',
                'user_access_course_lesson',
                'user_access_lesson_fragment',
            ),
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
    readonly_fields = ('get_avatar', )
    filter_horizontal = (
        'groups',
        'user_permissions',
        'user_access_course',
        'user_access_course_theme',
        'user_access_course_lesson',
        'user_access_lesson_fragment',
    )

    def get_avatar(self, obj):
        avatar = obj.avatar.url
        avatar = avatar.replace('media/', '') if 'static' in avatar else avatar

        return mark_safe(
            '<img src="%s" width="150" height="150" />' % avatar
        )
    get_avatar.short_description = 'Аватар'
