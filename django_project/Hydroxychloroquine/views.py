from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import views as auth_views
from django_email_verification import sendConfirm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.template import loader

from django.http import HttpResponseRedirect
from .testingVars import test_buildings, test_building_names, test_reports
from django.forms import formset_factory
from . import forms
from . import models

# for display purposes
max_num_excursions = 5

def convert_to_24_hour_time(t):
    if t[-2:]=='pm':
        splits=t.split(":")
        hour=splits[0]
        splits[0]=str(int(hour)+12) if not int(hour)==12 else "0"
        t=":".join(splits)
    return t

@require_POST
@login_required
def Remove_building(request):
    user = request.user
    excursion_id = request.POST.get('excursion_id', None)
    excursion = models.Excursion.objects.get(id=excursion_id)
    if user==excursion.user_id:
        print("  ***deleting excursion object***  excursion =",excursion )
        excursion.delete()
    context = {
        'building_id': excursion_id
    }
    # context = {'building_id': excursion.building_id} # mabye we want to say something back?
    # return HttpResponse(json.dumps(context), content_type='application/json') # maybe alternative method
    return JsonResponse(context)

def home(request):
    context = {"title": "home",}
    return render(request, "Hydroxychloroquine/home.html", context)

def data(request):
    print(request.method)
    reportNum = models.Report.objects.count()
    reports={}
    r = models.Report.objects.all()
    for x in reversed(range(reportNum)):
        tempDict = {}
        tempDict["TestDate"]=r[x].date_of_test
        userType = models.CustomUser.objects.values_list("user_type", flat = True).filter(id = r[x].user_id_id)
        if userType[0] == 'O':
            tempDict["Position"]= "Other"
        elif userType[0] == 'STU':
            tempDict["Position"]= "Student"
        else:
            tempDict["Position"]= "Staff"
        tempDict["DateLastOnCampus"]=r[x].date_last_on_campus
        buildingList = []
        eList = []
        buildingString = ""
        #finding the 
        eList = list(dict.fromkeys(models.Excursion.objects.filter(report_id_id=(r[x].id)).values_list("building_id_id", flat=True)))
        for n in eList:
            temp = n
            buildingList +=models.Building.objects.filter( building_id=temp ).values_list("building_name", flat=True)
        buildingList = list(dict.fromkeys(buildingList))
        for n in buildingList:
            buildingString += n +", "
        buildingString= buildingString[:len(buildingString)-2]
        tempDict["BuildingsImpacted"]= buildingString
        reports[str(r[x].id)] = tempDict
    context = {
        "title": "data",
        "recent_reports": reports,
    }
    return render(request, "Hydroxychloroquine/data.html", context)


@login_required
def account(request):
    SelectBuildingFormSet = formset_factory(forms.SelectBuildingForm, extra=max_num_excursions, max_num=max_num_excursions)

    # userchange form
    if request.method == "POST" and 'username_change' in request.POST:
        form_userchange = forms.CustomUserChangeForm(request.POST, instance=request.user)
        if form_userchange.is_valid():
            form_userchange.save(commit=True)
            print("  ***username changed***")
            return redirect("Hydroxychloroquine-account")
    else:
        form_userchange = forms.CustomUserChangeForm(instance=request.user)

    # formset_SelectBuilding
    if request.method == "POST" and 'add_buildings' in request.POST:
        formset_SelectBuilding = SelectBuildingFormSet(request.POST, prefix="excursions")
        formset_SelectBuilding_valid=any(form.is_valid() for form in formset_SelectBuilding)
        for form in formset_SelectBuilding:
            if form.is_valid():
                # make excursion object
                e = models.Excursion.objects.create(
                    user_id = request.user,
                    building_id = form.cleaned_data['building_id'],
                    start_time = convert_to_24_hour_time(form.cleaned_data['start_time']),
                    end_time = convert_to_24_hour_time(form.cleaned_data['end_time']),
                    )
                print("  ***excursion object made***  excursion =",e)
        return redirect("Hydroxychloroquine-account")
    else:
        formset_SelectBuilding = SelectBuildingFormSet(prefix="excursions")

    users_excursions = models.Excursion.objects.filter(user_id=request.user).filter(report_id=None)
    context = {
        "title": "account",
        "loop_max": len(formset_SelectBuilding) - 1,
        "form_userchange": form_userchange,
        "formset_SelectBuilding": formset_SelectBuilding,
        "users_excursions": users_excursions,
    }
    return render(request, "Hydroxychloroquine/account.html", context)


@login_required
def reportTest(request):
    SelectBuildingFormSet = formset_factory(
        forms.SelectBuildingForm, extra=max_num_excursions, max_num=max_num_excursions
    )
    if request.method == "POST":
        report_form = forms.ReportTestForm(request.POST)
        formset_SelectBuilding = SelectBuildingFormSet(request.POST, prefix="excursions")
        SelectBuilding_valid=any(form.is_valid() for form in formset_SelectBuilding) and report_form.is_valid()
        if SelectBuilding_valid:
            # make report object
            r = models.Report.objects.create(
                user_id=request.user,
                date_of_test=report_form.cleaned_data["date_of_test"],
                date_last_on_campus=report_form.cleaned_data["date_of_test"],
            )
            print("  ***report object made***  excursion =",r)

            # make excursion objects accociated with report
            for form in formset_SelectBuilding:
                if form.is_valid():
                    e = models.Excursion.objects.create(
                        report_id = r,
                        user_id = request.user,
                        building_id = form.cleaned_data['building_id'],
                        start_time = convert_to_24_hour_time(form.cleaned_data['start_time']),
                        end_time = convert_to_24_hour_time(form.cleaned_data['end_time']),
                        )
                    print("  ***excursion object made***  excursion =",e)

            # Send email to effected users
            if True:
                # finding all the building impacted
                buildingList = []
                emailList = []
                usersAffected = []
                # find the last report submitted ^
                reportId = models.Report.objects.values_list("id").last()
                rId = reportId[0]
                # adding the buildings impacted in that report^
                eList = list(
                    models.Excursion.objects.filter(report_id_id=rId).values_list(
                        "building_id_id", flat=True
                    )
                )
                for x in eList:
                    temp = x
                    # getting the builing names
                    buildingList += list(
                        dict.fromkeys(
                            models.Building.objects.filter(
                                building_id=temp
                            ).values_list("building_name", flat=True)
                        )
                    )
                # finding all of the users with the buildings added and effected
                for x in eList:
                    usersAffected = models.Excursion.objects.filter(building_id_id = x).exclude(
                    report_id__isnull=False
                    ).values_list("user_id", flat=True)
                usersAffected = list(dict.fromkeys(usersAffected))
                # grabbing their emails
                for x in usersAffected:
                    temp = x
                    emailList += list(
                        models.CustomUser.objects.filter(id=temp).values_list(
                            "email", flat=True
                        )
                    )
                # Insert code to send email
                html_message = loader.render_to_string(
                        'Hydroxychloroquine/report_mail.html',
                        {
                            'body': 'A positive COVID-19 test has been reported in one of the buildings you have selected. Please visit the website to see the buildings were affected.'
                        }
                    )
                send_mail(
                    "Positive COVID-19 test reported",
                    "A positive COVID-19 test has been reported in one of the buildings you have selected. Please visit the website to see the buildings were affected.",
                    "hydroxy.app@gmail.com",
                    emailList,
                    html_message = html_message
                )
            return redirect("Hydroxychloroquine-home")
        else:
            #TODO: prevent user form navgating if report is not valid
            pass
    else:
        report_form = forms.ReportTestForm()
        formset_SelectBuilding = SelectBuildingFormSet(prefix="excursions")
    context = {
        "title": "account",
        "loop_max": len(formset_SelectBuilding) - 1,
        "report_form": report_form,
        "formset_SelectBuilding": formset_SelectBuilding,
    }

    return render(request, "Hydroxychloroquine/reportTest.html", context)



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
