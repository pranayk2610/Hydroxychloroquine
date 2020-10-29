from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django_email_verification import sendConfirm

# from django.http import HttpResponse
from .testingVars import test_buildings, test_reports
from .forms import UserRegistrationForm

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
    context = {
        "title": "account",
        "buildings": test_buildings,
        "times": display_times,
        "max_num_excursions_counter": range(1, 1 + max_num_excursions),
    }
    return render(request, "Hydroxychloroquine/account.html", context)


def reportTest(request):
    context = {
        "title": "reportTest",
        "buildings": test_buildings,
        "times": display_times,
        "max_num_excursions_counter": range(1, 1 + max_num_excursions),
    }
    return render(request, "Hydroxychloroquine/reportTest.html", context)


def selectBuildings(request):
    context = {
        "title": "selectBuildings",
    }
    return render(request, "Hydroxychloroquine/selectBuildings.html", context)


def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            sendConfirm(user)
            return redirect("Hydroxychloroquine-login")
    else:
        form = UserRegistrationForm()
    return render(request, "Hydroxychloroquine/signup.html", {"form": form})


def forgotPassword(request):
    context = {
        "title": "forgotPassword",
    }
    return render(request, "Hydroxychloroquine/forgotPassword.html", context)
