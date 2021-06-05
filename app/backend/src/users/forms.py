from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.exceptions import ValidationError

from courses.models import Course
from courses_access.models import Access
from dialogs.models import Dialog, DialogMessage
from users import permissions
from users.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        with transaction.atomic():

            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            user.save()

            course = Course.objects.order_by('id').first()
            if course:
                access, created = Access.objects.get_or_create(
                    user=user, course=course, status=Access.COURSE_ACCESS_TYPE_TRIAL
                )
                if created:
                    access.set_trial()

            educator = User.reviewers.get_less_busy_educator()
            user.reviewer = educator

            support = User.supports.get_less_busy_support()
            user.support = support
            user.save()

            dialog_with_educator = Dialog.objects.create()
            dialog_with_educator.with_role = permissions.GROUP_EDUCATOR
            dialog_with_educator.users.add(user, educator)
            dialog_with_educator.save()

            dialog_with_support = Dialog.objects.create()
            dialog_with_support.with_role = permissions.GROUP_SUPPORT
            dialog_with_support.users.add(user, support)
            dialog_with_support.save()

            DialogMessage.objects.create_hello_educator(dialog_with_educator, from_user=educator, student=user)
            DialogMessage.objects.create_hello_support(dialog_with_support, from_user=support, student=user)

        return user
