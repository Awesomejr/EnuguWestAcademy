import logging
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model

from .models import Session, CustomUser
from .forms import LoginForm, UpdateUserForm2, ChangePasswordForm

from utilities import customFuncs
# from utilities import initializeDB

logger = logging.getLogger(__name__)
CURRENT_SESSION = customFuncs.getCurrentSession(Session)


# Create your views here.
def index(request):
    form = LoginForm()
    context = {"form": form}
    return render(request, "base/pages/index.html", context=context)


def loginUser(request):
    user = None
    redirect_link = "base:home"

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            logger.info("Login attempted detected!!!")
            username = str(form.cleaned_data.get("username")).strip()
            password = str(form.cleaned_data.get("password")).strip()
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                logger.info("User Not Found!!!")
                messages.error(request, "Incorrect Username or Password!!!")
                return redirect("base:login")

            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_suspended == False and user.is_deleted == False: 
                login(request, user)
                user.last_login = datetime.datetime.now()
                return redirect("base:dashboard")
            elif user is not None and user.is_suspended == True:
                messages.info(request, 
                        f"You have been suspended from accessing this site. Kindly contact the site administrator for more info.".capitalize()
                    )
                return redirect(redirect_link)
            elif user is not None and user.is_deleted == True:
                messages.error(request, 
                        f"Account not found!!!".capitalize()
                    )
                return redirect(redirect_link)
            elif user is not None and user.is_active == False:
                messages.error(request, f"You have been deactivated from accessing this site. Kindly contact the site administartor for more info.".capitalize())
                return redirect(redirect_link)
            else:
                messages.error(request, "Incorrect Username or Password!!!")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    return redirect(redirect_link)


@login_required(login_url="base:home")
def dashboard(request):
    user = CustomUser.objects.get(id=request.user.id)
    if  user.is_suspended:
        messages.info(request, 
                        f"You have been suspended from accessing your dasboard. Kindly contact the site administrator/tech support for more info.".capitalize()
                    )
        return redirect("base:home")
    elif user.role == "tech_support" or user.role == "mini_tech_support" or \
                user.role =="academic_director" or user.is_superuser:
        return redirect("techsupport:dashboard")
    elif user.role =="data_entry":
        return redirect("techsupport:createTopic")
    elif user.role == "student":
        return redirect("student:dashboard")
    elif user.role == "teacher":
        return redirect("teacher:dashboard")
    elif user.role == "parent":
        messages.info(request, f"You can't access your dashboard now. Try again later".capitalize())
        return redirect("base:home")
    elif user.role == "guest":
        return redirect("guest:dashboard")
    elif user.role == "manager" or user.role == "mini_manager":
        return redirect("manager:dashboard")
    else:
        messages.info(request, 
                    f"You can't access your dashboard because a role have not been assigned to you yet. Try again later".capitalize()
                )


@login_required(login_url="base:home")
def userAccount(request):
    custom_user = request.user

    if custom_user.is_suspended:
        messages.info(request, 
                        f"You have been suspended from accessing your dasboard. Kindly contact the site administrator/tech support for more info.".capitalize()
                    )
        return redirect("base:home")
    
    initial_data = {
        "first_name": custom_user.first_name,
        "last_name": custom_user.last_name,
        "middle_name": custom_user.middle_name,
        "username": custom_user.username,
        "email": custom_user.email,
    }
    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, object_name="User Account/Profile")
        form = UpdateUserForm2(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            logger.debug(f"Cleaned Data: {form.cleaned_data}")
            email = form.cleaned_data.get("email")
            avatar = form.cleaned_data.get("avatar")
            if avatar:
                try:
                    custom_user.avatar = customFuncs.resizeImage(avatar)
                except:
                    pass
            custom_user.email = email
            custom_user.save()
            
            logger.debug(f"Cleanded_data: {form.cleaned_data}")
            logger.info(f"Profile has been updated successfully.".capitalize())
            messages.success(request, f"Profile has been updated successfully.".capitalize())
            return redirect("base:userAccount")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = UpdateUserForm2(initial=initial_data)
        change_password_form = ChangePasswordForm()

    context = {"form": form, "custom_user": custom_user, "change_password_form": change_password_form}

    return render(request, "./base/pages/userAccount.html", context=context)


@login_required(login_url="base:home")
def changeUserPassword(request):
    redirect_link = "base:userAccount"

    if request.method == "POST":
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            current_password = change_password_form.cleaned_data.get("current_password")
            new_password1 = change_password_form.cleaned_data.get("new_password1")
            new_password2 = change_password_form.cleaned_data.get("new_password2")

            if new_password1 != new_password2:
                messages.error(request, f"New password and re-entered password does not match!!!".capitalize())
                return redirect(redirect_link)

            user = authenticate(request, username=request.user.username, password=current_password)
            if user is not None:
                user.set_password(new_password1)
                user.save()
                logger.info(f"Password has been updated successfully.".capitalize())
                messages.success(request, f"Passowrd has been updated successfully.".capitalize())
                return redirect(redirect_link)
            else:
                messages.error(request, f"You are not authorized to modify this password!!!".capitalize())
                return redirect(redirect_link)

        else:
            customFuncs.displayFormErrors(request, change_password_form, messages, logger)
    else:
        redirect(redirect_link)

    return redirect(redirect_link)


@login_required(login_url="base:home")
def userProfile(request):
    return render(request, "./base/pages/userProfile.html")


@login_required(login_url="base:home")
def deleteAllRequestsLogs(request):
    customFuncs.deleteAllRequestsLogs()
    messages.success(request, f"All Site Request Logs Has Been Delete")
    return redirect("base:dashboard")

def logoutConfirmation(request):
    logger.info(f"{request.user.getFullName} is attempting user logout")
    return render(request, "./base/pages/logoutConfirmation.html")


@login_required(login_url="base:home")
def logoutUser(request):
    messages.success(request, f"Username '{request.user.username}' have been logged out.")
    logger.info(f"Username '{request.user.username}' have been logged out.")
    logout(request)
    return redirect("base:home")