from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from courses_access.models.course import CourseAccess
from courses.models import Course


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
        if commit:
            user.save()

        # При регистрации юзера даем ему триал-доступ к курсу
        # Если проводилась регистрация персонала (Ревьюер), то предоставить полный доступ к курсу  # TODO:
        course = Course.objects.first()
        CourseAccess.objects.set_trial(course, user)

        return user
