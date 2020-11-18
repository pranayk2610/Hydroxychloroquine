from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django_email_verification import sendConfirm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse

from django.http import HttpResponse, HttpResponseRedirect
from .testingVars import test_buildings, test_building_names, test_reports
from django.forms import formset_factory
from . import forms
from . import models

# from . import view_templates

# for display purposes
max_num_excursions = 2

<<<<<<< HEAD
=======
def Remove_building(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)
>>>>>>> edee73ab242306380b02f4351ff965719713464a

def home(request):
    print(request.method)

    context = {
        "title": "home",
        "recent_reports": test_reports,
    }
    return render(request, "Hydroxychloroquine/home.html", context)

def data(request):
    print(request.method)

    context = {
        "title": "data",
        "recent_reports": test_reports,
    }
    return render(request, "Hydroxychloroquine/data.html", context)

@login_required
def account(request):
    SelectBuildingFormSet = formset_factory(forms.SelectBuildingForm, extra=max_num_excursions, max_num=max_num_excursions)

    # userchange form
    if request.method == "POST":
        form_userchange = forms.CustomUserChangeForm(request.POST, instance=request.user)
        if form_userchange.is_valid():
            form_userchange.save(commit=True)
            print("  ***username changed***")
            return redirect("Hydroxychloroquine-account")
    else:
        form_userchange = forms.CustomUserChangeForm(instance=request.user)

    # formset_SelectBuilding
<<<<<<< HEAD
    SelectBuildingFormSet = formset_factory(
        forms.SelectBuildingForm, extra=max_num_excursions, max_num=max_num_excursions
    )
=======
>>>>>>> edee73ab242306380b02f4351ff965719713464a
    if request.method == "POST":
        formset_SelectBuilding = SelectBuildingFormSet(
            request.POST, prefix="excursions"
        )
        print("formset_SelectBuilding.is_valid():", formset_SelectBuilding.is_valid())
        # if formset_SelectBuilding.is_valid():
        for form in formset_SelectBuilding:
            if form.is_valid():
                # make excursion object
                print("  ***creating excursion object***")
                for f in list(form.fields):
                    print("form.cleaned_data:", form.cleaned_data)
                    print("field:", f, "| data=", form[f].value())
                    # print("field:",f,"choice=", form.fields[f].choices)
                    print("field:", f, "| cleaned data=", form.cleaned_data[f])
                e = models.Excursion.objects.create(
                    user_id=request.user,
                    building_id=form.cleaned_data["building_id"],
                    start_time=form.cleaned_data["start_time"],
                    end_time=form.cleaned_data["end_time"],
                )
                print("  ***excursion object made***")

    else:
        formset_SelectBuilding = SelectBuildingFormSet(prefix="excursions")

<<<<<<< HEAD
    # userchange form
    if request.method == "POST":
        form_userchange = forms.CustomUserChangeForm(
            request.POST, instance=request.user
        )
        if form_userchange.is_valid():
            form_userchange.save(commit=True)
            return redirect("Hydroxychloroquine-account")
    else:
        form_userchange = forms.CustomUserChangeForm(instance=request.user)
=======
>>>>>>> edee73ab242306380b02f4351ff965719713464a

    context = {
        "title": "account",
        "buildings": list(models.Building.objects.all()),
        "times": [
            "{}:00{}".format(h, ap)
            for ap in ("am", "pm")
            for h in ([12] + list(range(1, 12)))
        ],
        "max_num_excursions_counter": range(1, 1 + max_num_excursions),
        "loop_max": len(formset_SelectBuilding) - 1,
        "form_userchange": form_userchange,
        "formset_SelectBuilding": formset_SelectBuilding,
        "users_excursions": models.Excursion.objects.filter(user_id=request.user).filter(report_id=None),
    }

    return render(request, "Hydroxychloroquine/account.html", context)

@login_required
def reportTest(request):
    """
    models.Building.objects.all().delete()
    for i,n in enumerate(test_building_names, start=1):
        n=str(n)
        e = models.Building.objects.create(
            building_id = int(i),
            building_name = str(n),
            )
    """
    # print(e)
    # for x in models.Building.objects.all(): print(x)
    # print(models.Building.objects.first())

    # for x in models.Building.objects.all(): print(str(x.building_name))
    # print(models.Building.objects.all().values('building_name') )
    SelectBuildingFormSet = formset_factory(
        forms.SelectBuildingForm, extra=max_num_excursions, max_num=max_num_excursions
    )
    if request.method == "POST":
        # models.Excursion.objects.all().delete()
        # models.Report.objects.all().delete()
        report_form = forms.ReportTestForm(request.POST)
        formset_SelectBuilding = SelectBuildingFormSet(
            request.POST, prefix="excursions"
        )
        print("report_form.is_valid():", report_form.is_valid())
        print("formset_SelectBuilding.is_valid():", formset_SelectBuilding.is_valid())
        report_made = False
        if report_form.is_valid():
            for form in formset_SelectBuilding:
                if form.is_valid():
                    # make report if first valid form
                    if not report_made:
                        print("  ***creating report object***")
                        for f in list(report_form.fields):
                            print("field:", f, "| data=", report_form.cleaned_data[f])
                            r = models.Report.objects.create(
                                user_id=request.user,
                                date_of_test=report_form.cleaned_data["date_of_test"],
                                date_last_on_campus=report_form.cleaned_data[
                                    "date_of_test"
                                ],
                            )
                        print("  ***report object made***")
                        report_made = True

                    # make excursion object and accociate with report
                    print("  ***creating excursion object***")
                    for f in list(form.fields):
                        print("form.cleaned_data:", form.cleaned_data)
                        print("field:", f, "| data=", form[f].value())
                        # print("field:",f,"choice=", form.fields[f].choices)
                        print("field:", f, "| cleaned data=", form.cleaned_data[f])
                    e = models.Excursion.objects.create(
                        report_id=r,
                        user_id=request.user,
                        building_id=form.cleaned_data["building_id"],
                        start_time=form.cleaned_data["start_time"],
                        end_time=form.cleaned_data["end_time"],
                    )
                    print("  ***excursion object made***")
            if report_made:
                #finding all the building impacted
                buildingList = []
                emailList = []
                #find the last report submitted ^
                reportId = models.Report.objects.values_list('id').last()
                rId = reportId[0]
                #adding the buildings impacted in that report^
                eList = list(models.Excursion.objects.filter(report_id_id = rId).values_list('building_id_id', flat = True))
                for x in eList:
                    temp = x
                    #getting the builing names
                    buildingList += list( dict.fromkeys(models.Building.objects.filter(building_id = temp).values_list('building_id', flat = True)))
                #finding all of the users with the buildings added and effected
                eList = models.Excursion.objects.exclude(report_id__isnull = False).values_list('user_id', flat = True)
                eList = list( dict.fromkeys(eList) )
                #grabbing their emails
                for x in eList:
                    temp = x
                    emailList += list(models.CustomUser.objects.filter(id = temp).values_list('email', flat = True))
                # Insert code to send email
                send_mail("Positive COVID-19 test reported", "A positive COVID-19 test has been reported in one of the buildings you have selected", "hydroxy.app@gmail.com", emailList)
            return redirect("Hydroxychloroquine-home")
        else:
            return redirect("Hydroxychloroquine-account")
    else:
        report_form = forms.ReportTestForm()
        formset_SelectBuilding = SelectBuildingFormSet(prefix="excursions")
    context = {
        "title": "account",
        "buildings": list(models.Building.objects.all()),
        "times": [
            "{}:00{}".format(h, ap)
            for ap in ("am", "pm")
            for h in ([12] + list(range(1, 12)))
        ],
        "max_num_excursions_counter": range(1, 1 + max_num_excursions),
        "loop_max": len(formset_SelectBuilding) - 1,
        "report_form": report_form,
        "formset_SelectBuilding": formset_SelectBuilding,
    }

    return render(request, "Hydroxychloroquine/reportTest.html", context)


def selectBuildings(request):
    print("selectBuildings requested")

    # if request.method == "POST":
    #     form = forms.ReportTestForm(request.POST)
    #     print('request.method == "POST"')
    #     print('form.is_valid():',form.is_valid())
    #     if form.is_valid():
    #         # print("form.cleaned_data",form.cleaned_data)
    #         print("***creating excursion objects***")
    #         r = models.Excursion.objects.create(
    #             date_of_test = form.cleaned_data['date_of_test'],
    #             date_last_on_campus = form.cleaned_data['date_of_test'],
    #             user_id = request.user,
    #             )
    #         return redirect("Hydroxychloroquine-home")
    #     else:
    #         return redirect("Hydroxychloroquine-account")
    # else:
    #     print('request.method != "POST"')
    #     form = forms.ReportTestForm()
    context = {
        "title": "selectBuildings",
    }
    return render(request, "Hydroxychloroquine/selectBuildings.html", context)


def signup(request):
    if request.user.is_authenticated:
        redirect("Hydroxychloroquine-home")
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
                v = form.errors.get_json_data()[k][0]["message"]
                messages.error(request, v)
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
    print(request.method)
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
    print(request.method)
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
