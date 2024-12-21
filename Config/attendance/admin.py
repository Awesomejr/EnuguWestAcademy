from django.contrib import admin

from .models import StudentAttendance, TeacherAttendance


# Register your models here.
@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'student',
        'school_branch',
        'class_name',
        'date',
        'status',
        'reason_for_absence',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'student',
        'school_branch',
        'class_name',
        'date',
    )


@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'teacher',
        'date',
        'status',
        'reason_for_absence',
    )
    list_filter = ('created_on', 'updated_on', 'teacher', 'date')
