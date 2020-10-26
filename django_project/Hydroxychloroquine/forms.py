from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email", "password1", "password2")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
