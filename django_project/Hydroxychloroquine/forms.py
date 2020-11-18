from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django import forms as django_forms
from django.utils import timezone

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


class ExcursionForm(ModelForm):
    class Meta:
        model = models.Excursion
        fields = ['report_id', 'user_id', 'building_id', 'start_time', 'end_time']


class SelectBuildingForm(django_forms.Form):
    building_id = django_forms.ModelChoiceField(
        queryset=models.Building.objects.all(),
        # widget=forms.Select(attrs={'class': 'form-control', 'required': True})
        # to_field_name="building_id",
        # initial=models.Building.objects.first(),
        required = False,
        )
    times = ['{}:00{}'.format(h, ap) for ap in ('am', 'pm') for h in ([12] + list(range(1,12)))]
    time_choices = [(t,t) for i,t in enumerate(times,start=1)]
    # time_choices = [(i,t) for i,t in enumerate(times,start=1)]
    start_time = django_forms.ChoiceField(
        label="Start Time",
        choices=time_choices,
        # initial="12:00am",
        required = False,
    )
    end_time = django_forms.ChoiceField(
        label="End Time",
        choices=time_choices,
        # initial="11:00pm",
        required = False,
    )


class ReportTestForm(django_forms.Form):
    # incomplete
    # based on https://stackoverflow.com/questions/61461129/django-radio-buttons-appearing-as-bullet-point-list-inside-mark-safe
    test_result_choices = [(1, "Positive"), (2, "Negative")]
    test_result = django_forms.ChoiceField(
        widget=django_forms.RadioSelect(),
        label="Was your COVID-19 test result positive or negative?",
        choices=test_result_choices,
        initial=1,
    )
    date_of_test = django_forms.DateField(
        label="On what date did the test occur?",
        # initial=make_aware(datetime.now()).date(),
        # initial=datetime.date(),
        initial=timezone.now().date(),
    )
    user_type_choices = [(1, "Student"), (2, "Faculty"), (3, "Staff"), (4, "Other")]
    user_type = django_forms.ChoiceField(
        widget=django_forms.RadioSelect(),
        label="Which category do you fall in?",
        choices=user_type_choices,
        initial=1,
    )
