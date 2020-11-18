from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ajax/Remove_building/$', views.Remove_building, name='Remove_building'),
    path("", views.home, name="Hydroxychloroquine-home"),
    path("home/", views.home, name="Hydroxychloroquine-home"),
    path("data/", views.data, name="Hydroxychloroquine-data"),
    path("account/", views.account, name="Hydroxychloroquine-account"),
    path("reportTest/", views.reportTest, name="Hydroxychloroquine-reportTest"),
    path(
        "selectBuildings/",
        views.selectBuildings,
        name="Hydroxychloroquine-selectBuildings",
    ),
    path("signup/", views.signup, name="Hydroxychloroquine-signup"),
    path("login/", views.login, name="Hydroxychloroquine-login"),
    path("logout/", views.logout, name="Hydroxychloroquine-logout"),
    path(
        "passwordReset/",
        views.passwordReset,
        name="password_reset",
    ),
    path(
        "passwordReset/done/",
        views.passwordResetDone,
        name="password_reset_done",
    ),
    path(
        "passwordResetConfirm/<uidb64>/<token>/",
        views.passwordResetConfirm,
        name="password_reset_confirm",
    ),
    path(
        "passwordResetComplete/",
        views.passwordResetComplete,
        name="password_reset_complete",
    ),
    path(
        "passwordChange/",
        views.passwordChange,
        name="password_change",
    ),
    path(
        "passwordChange/done/",
        views.passwordChangeDone,
        name="password_change_done",
    ),
]
