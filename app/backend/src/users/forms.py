from django import forms
from django.core.exceptions import ValidationError

from courses.models import Course
from courses_access.models import Access
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
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()

        # При регистрации юзера даем ему триал-доступ к курсу
        course = Course.objects.first()
        access, created = Access.objects.get_or_create(user=user, course=course, status=Access.COURSE_ACCESS_TYPE_TRIAL)

        if created:
            access.set_trial()

        educator = User.reviewers.get_less_busy_educator()
        user.reviewer = educator
        user.save()

        return user
