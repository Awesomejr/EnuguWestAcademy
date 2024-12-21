from django.urls import path

from . import views


app_name = "guest"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("view-initials/", views.viewInitials, name="viewInitials"),
    
    path("students-attendance/", views.studentsAttendance, name="studentsAttendance"),
    path("view-student-attendance/<uuid:studentId>", views.viewStudentAttendance, name="viewStudentAttendance"),
    
    path("view-students/", views.viewStudents, name="viewStudents"),

    path("view-parents/", views.viewParents, name="viewParents"),

    path("view-teachers/", views.viewTeachers, name="viewTeachers"),
    path("teachers-attendance/", views.teacherAttendance, name="teacherAttendance"),
    path("view-teacher-attendance/<uuid:teacherId>/", views.viewTeacherAttendance, name="viewTeacherAttendance"),
]