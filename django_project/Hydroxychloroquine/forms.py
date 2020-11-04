from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django import forms as django_forms

from . import models


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = models.CustomUser
        fields = ("display_name", "email", "password1", "password2")


class CustomUserChangeForm(ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ("display_name",)


class CustomAuthenticationForm(AuthenticationForm):
    RememberMe = django_forms.BooleanField(
        label="Remember Me", widget=django_forms.CheckboxInput, required=False
    )


class ReportTestForm(django_forms.Form):
    # incomplete
    # based on https://stackoverflow.com/questions/61461129/django-radio-buttons-appearing-as-bullet-point-list-inside-mark-safe
    test_result_choices = [(1, "Positive"), (2, "Negative")]
    test_result = django_forms.ChoiceField(
        widget=django_forms.RadioSelect(),
        label="Was your COVID-19 test result positive or negative?",
        choices=test_result_choices,
    )
    test_date = django_forms.DateField(
        label="On what date did the test occur?",
    )
    user_type_choices = [(1, "Student"), (2, "Faculty"), (3, "Staff"), (4, "Other")]
    user_type = django_forms.ChoiceField(
        widget=django_forms.RadioSelect(),
        label="Which category do you fall in?",
        choices=user_type_choices,
    )
