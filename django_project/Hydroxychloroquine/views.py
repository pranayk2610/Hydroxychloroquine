from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django_email_verification import sendConfirm
from django.contrib import messages
from django.core.exceptions import ValidationError

from django.http import HttpResponse, HttpResponseRedirect
from .testingVars import test_buildings, test_reports
from . import forms

# from . import view_templates

# for display purposes
max_num_excursions = 5

# list used in displaying buildings in account.html and reportTest.html
# (invoked in a call to selectBuildings.html)
display_times = [
    "12:00AM",
    "1:00AM",
    "2:00AM",
    "3:00AM",
    "4:00AM",
    "5:00AM",
    "6:00AM",
    "7:00AM",
    "8:00AM",
    "9:00AM",
    "10:00AM",
    "11:00AM",
    "12:00PM",
    "1:00PM",
    "2:00PM",
    "3:00PM",
    "4:00PM",
    "5:00PM",
    "6:00PM",
    "7:00PM",
    "8:00PM",
    "9:00PM",
    "10:00PM",
    "11:00PM",
]


def home(request):
    context = {
        "title": "home",
        "recent_reports": test_reports,
    }
    return render(request, "Hydroxychloroquine/home.html", context)


@login_required
def account(request):
    if request.method == "POST":
        form = forms.CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save(commit=True)
            return redirect("Hydroxychloroquine-account")
    else:
        form = forms.CustomUserChangeForm(instance=request.user)
    context = {
        "title": "account",
        "buildings": test_buildings,
        "times": display_times,
        "max_num_excursions_counter": range(1, 1 + max_num_excursions),
        "loop_max": max_num_excursions,
        "form": form,
    }
    return render(request, "Hydroxychloroquine/account.html", context)


def reportTest(request):
    if request.method == "POST":
        form = forms.ReportTestForm(request.POST)
        if form.is_valid():
            return redirect("Hydroxychloroquine-home")
    else:
        form = forms.ReportTestForm()

    context = {
        "title": "account",
        "buildings": test_buildings,
        "times": display_times,
        "max_num_excursions_counter": range(1, 1 + max_num_excursions),
        "loop_max": max_num_excursions,
        "form": form,
    }
    return render(request, "Hydroxychloroquine/reportTest.html", context)


def selectBuildings(request):
    context = {
        "title": "selectBuildings",
    }
    return render(request, "Hydroxychloroquine/selectBuildings.html", context)


def signup(request):
    if request.method == "POST":
        form = forms.UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            sendConfirm(user)
            return redirect("Hydroxychloroquine-login")
        else:
            for k in form.errors.get_json_data():
                v=form.errors.get_json_data()[k][0]['message']
                messages.error(request,v)
                # print(v)
    else:
        form = forms.UserRegistrationForm()
    return render(request, "Hydroxychloroquine/signup.html", {"form": form})


def forgotPassword(request):
    context = {
        "title": "forgotPassword",
    }
    return render(request, "Hydroxychloroquine/forgotPassword.html", context)


# view template
def login(request, *args, **kwargs):
    if request.method == "POST":
        if not request.POST.get("RememberMe", None):
            request.session.set_expiry(0)

    # debug print to terminal start
    # if request.method == "POST":
    #     if not request.POST.get("RememberMe", None):
    #         print("RememberMe was unchecked")
    #     else:
    #         print("RememberMe was checked")
    #     print(request.POST.get("RememberMe"))
    #     print("Login expires in {} seconds".format(request.session.get_expiry_age()))
    #     print(
    #         "Login expires at browser close:",
    #         request.session.get_expire_at_browser_close(),
    #     )
    # debug print to terminal end

    customRender = auth_views.LoginView.as_view(
        template_name="Hydroxychloroquine/login.html",
        redirect_authenticated_user=True,
        authentication_form=forms.CustomAuthenticationForm,
    )
    return customRender(request, *args, **kwargs)


def logout(request, *args, **kwargs):
    customRender = auth_views.LogoutView.as_view(
        template_name="Hydroxychloroquine/logout.html"
    )
    return customRender(request, *args, **kwargs)


def passwordReset(request, *args, **kwargs):
    customRender = auth_views.PasswordResetView.as_view(
        template_name="Hydroxychloroquine/forgotPassword.html"
    )
    return customRender(request, *args, **kwargs)


def passwordResetDone(request, *args, **kwargs):
    customRender = auth_views.PasswordResetDoneView.as_view(
        template_name="Hydroxychloroquine/passwordResetDone.html"
    )
    return customRender(request, *args, **kwargs)


def passwordResetConfirm(request, *args, **kwargs):
    customRender = auth_views.PasswordResetConfirmView.as_view(
        template_name="Hydroxychloroquine/passwordResetConfirm.html"
    )
    return customRender(request, *args, **kwargs)


def passwordResetComplete(request, *args, **kwargs):
    customRender = auth_views.PasswordResetCompleteView.as_view(
        template_name="Hydroxychloroquine/passwordResetComplete.html"
    )
    return customRender(request, *args, **kwargs)


def passwordChange(request, *args, **kwargs):
    customRender = auth_views.PasswordChangeView.as_view(
        template_name="Hydroxychloroquine/passwordChange.html"
    )
    return customRender(request, *args, **kwargs)


def passwordChangeDone(request, *args, **kwargs):
    customRender = auth_views.PasswordChangeDoneView.as_view(
        template_name="Hydroxychloroquine/passwordChangeDone.html"
    )
    return customRender(request, *args, **kwargs)
