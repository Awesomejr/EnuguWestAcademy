from django.urls import path

from . import views


app_name = "manager"

urlpatterns = [
        path("dashboard/", views.dashboard, name="dashboard"),

        path("register-parent/", views.registerParent, name="registerParent"),
        path("register-student/<uuid:parentID>/", views.registerStudent, name="registerStudent"),
        path("register-teacher/", views.registerTeacher, name="registerTeacher"),

        path("view-students/", views.viewStudents, name="viewStudents"),
        path("edit-student/<uuid:studentId>/", views.editStudent, name="editStudent"),

        path("view-teachers/", views.viewTeachers, name="viewTeachers"),
        path("edit-teacher/<uuid:teacherId>/", views.editTeacher, name="editTeacher"),

        path("view-parents/", views.viewParents, name="viewParents"),
        path("view-parent/<uuid:parentId>/", views.viewParent, name="viewParent"),

        path("students-attendance/", views.studentsAttendance, name="studentsAttendance"),
        path("preview-students-marked-attendance/", views.previewStudentsMarkedAttendance, name="previewStudentsMarkedAttendance"),
        path("students-attendance-statistics/", views.studentsAttendanceStatistics, name="studentsAttendanceStatistics"),
        path("take-students-attendance/<str:class_id>/", views.takeStudentsAttendance, name="takeStudentsAttendance"),
        path("view-student-attendance/<uuid:studentId>/", views.viewStudentAttendance, name="viewStudentAttendance"),
        path("edit-student-attendance/<uuid:attendanceId>/", views.editStudentAttendance, name="editStudentAttendance"),

        path("teacher-attendance/", views.teacherAttendance, name="teacherAttendance"),
        path("view-teacher-attendance/<uuid:teacherId>/", views.viewTeacherAttendance, name="viewTeacherAttendance"),
        path("take-teacher-attendance/", 
                views.takeTeacherAttendance, name="takeTeacherAttendance"
                ),

        path("view-questions/", views.viewQuestions, name="viewQuestions"),
]