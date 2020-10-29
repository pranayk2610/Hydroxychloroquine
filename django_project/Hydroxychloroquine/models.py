from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class Role(models.Model):
    role_id = models.IntegerField(primary_key=True)
    role_name = models.CharField(max_length=128)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        STUDENT: "STU"
        STAFF: "STA"
        OTHER: "O"

    display_name = models.CharField(max_length=128, default="John Doe")
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    first_login = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # add UserType to this
    user_type = models.CharField(max_length=3, choices=UserType.choices, default="O")

    roles = models.ManyToManyField(Role)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.display_name


class Report(models.Model):
    date_of_test = models.DateTimeField()
    date_last_on_campus = models.DateTimeField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s" % (self.date_of_test, self.date_last_on_campus, self.user_id)


class Building(models.Model):
    building_id = models.IntegerField(primary_key=True)
    building_name = models.CharField(max_length=128)

    def __str__(self):
        return "%s %s" % (self.building_id, self.building_name)


class Excursion(models.Model):
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return "%s %s %s" % (self.report_id, self.start_time, self.end_time)