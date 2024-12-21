from django.urls import path

from . import views


app_name = "teacher"

urlpatterns = [
        path("dashboard/", views.dashboard, name="dashboard"),
        path("create-topic/", views.createTopic, name="createTopic"),
        path("view-class/", views.viewClass, name="viewClass"),
        path("load-class-students/<uuid:classId>/", views.loadClassStudents, name="loadClassStudents"),
        path("view-attendance/", views.viewAttendance, name="viewAttendance"),

        path("create-question/", views.createQuestion, name="createQuestion"),
        path("create-question/topics-options/", views.topicsOptions, name="topicsOptions"),
        path("edit-question/<uuid:questionId>/", views.editQuestion, name="editQuestion"),
        path("edit-question-options/<uuid:questionId>/", views.editQuestionOptions, name="editQuestionOptions"),
        path("view-question/", views.viewQuestions, name="viewQuestions"),
        path("view-question-with-options/<uuid:questionId>/", views.viewQuestionWIthOptions, name="viewQuestionWIthOptions"),
]