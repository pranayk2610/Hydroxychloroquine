from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.home, name="Hydroxychloroquine-home"),
    path("home/", views.home, name="Hydroxychloroquine-home"),
    path("account/", views.account, name="Hydroxychloroquine-account"),
    path(
        "forgotPassword/",
        views.forgotPassword,
        name="Hydroxychloroquine-forgotPassword",
    ),
    path("index/", views.index, name="Hydroxychloroquine-index"),
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
]
