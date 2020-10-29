from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.home, name="Hydroxychloroquine-home"),
    path("home/", views.home, name="Hydroxychloroquine-home"),
    path("account/", views.account, name="Hydroxychloroquine-account"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="Hydroxychloroquine/login.html"),
        name="Hydroxychloroquine-login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="Hydroxychloroquine/logout.html"),
        name="Hydroxychloroquine-logout",
    ),
    path("reportTest/", views.reportTest, name="Hydroxychloroquine-reportTest"),
    path(
        "selectBuildings/",
        views.selectBuildings,
        name="Hydroxychloroquine-selectBuildings",
    ),
    path("signup/", views.signup, name="Hydroxychloroquine-signup"),
    path(
        "passwordReset/",
        auth_views.PasswordResetView.as_view(
            template_name="Hydroxychloroquine/forgotPassword.html"
        ),
        name="password_reset",
    ),
    path(
        "passwordReset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="Hydroxychloroquine/passwordResetDone.html"
        ),
        name="password_reset_done",
    ),
    path(
        "passwordResetConfirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="Hydroxychloroquine/passwordResetConfirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "passwordResetComplete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="Hydroxychloroquine/passwordResetComplete.html"
        ),
        name="password_reset_complete",
    ),
]
