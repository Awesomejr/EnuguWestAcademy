from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = "base"

urlpatterns = [
    # Base Views
    path("", views.index, name="home"),
    path("login-user/", views.loginUser, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("user-account/", views.userAccount, name="userAccount"),
    path("user-profile/", views.userProfile, name="userProfile"),
    path("logout-confirmation/", views.logoutConfirmation, name="logoutConfirmation"),
    path("logout-user/", views.logoutUser, name="logoutUser"),
    path("change-user-password/", views.changeUserPassword, name="changeUserPassword"),
    path("delete-all-requests-logs/", views.deleteAllRequestsLogs, name="deleteAllRequestsLogs"),




    # Auth Views
    path("reset-password/", 
        auth_views.PasswordResetView.as_view(template_name="base/pages/password_reset_form.html"), 
        name="password_reset"),
    path("password_reset/done/", 
        auth_views.PasswordResetDoneView.as_view(template_name="base/pages/password_reset_done.html"), 
        name="password_reset_done"),
    path("reset/<uidb64>/<token>/", 
        auth_views.PasswordResetConfirmView.as_view(template_name="base/pages/password_reset_confirm.html"), 
        name="password_reset_confirm"),
    path("reset/done/", 
        auth_views.PasswordResetCompleteView.as_view(template_name="base/pages/password_reset_complete.html"), 
        name="password_reset_complete"),
]