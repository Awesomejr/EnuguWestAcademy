from django.urls import path

from . import views


app_name = "student"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("view-attendance/", views.viewAttendance, name="viewAttendance"),
    path("view-class/", views.viewClass, name="viewClass"),
    path("view-parent/", views.viewParent, name="viewParent"),

    path("view-examination/", views.viewExamination, name="viewExamination"),
    path("take-examination/<uuid:examId>/", views.takeExamination, name="takeExamination"), 
    path("examination-result/<uuid:examId>/", views.examResult, name="examResult"),

    path("view-cbt-examination/", views.viewCBTExamination, name="viewCBTExamination"),
    path("view-cbt-examination-instruction/<uuid:cbtCategoryId>/", views.viewCBTExaminationInstruction, name="viewCBTExaminationInstruction"), 
    path("take-cbt-examination/<uuid:cbtCategoryId>/", views.takeCBTExamination, name="takeCBTExamination"), 
    path("cbt-examination-result/<uuid:cbtCategoryId>/", views.cbtExamResult, name="cbtExamResult"),
    path("view-cbt-result/<uuid:cbtCategoryId>/", views.viewCBTExamResult, name="viewCBTExamResult"),
]