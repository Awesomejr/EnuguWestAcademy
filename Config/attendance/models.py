from django.db import models
from django.utils import timezone
from django.db.models import Count, Case, When, F, Avg, FloatField, Value

from base.models import TimeStamp, StudentProfile, TeacherProfile, Class, Session, CustomUser, SchoolBranch
from utilities.customVars import ATTENDANCE_STATUS


# Create your models here.
class StudentAttendance(TimeStamp):
    # Remove null fields in production: created_by, session, status, date
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="attendance_records")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    school_branch = models.ForeignKey(SchoolBranch, on_delete=models.CASCADE, null=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, null=True)
    status = models.CharField(max_length=40, choices=ATTENDANCE_STATUS, default="absent", null=True)
    reason_for_absence = models.TextField(null=True, blank=True)
    # teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="attendance_taken")
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,
                                    limit_choices_to={'role__in': ["teacher", "admin", "mini_tech_support", "tech_support", "superuser"]},
                                    related_name="student_attendance_taken"
                                    )

    def getStudentAttendanceScore(self):
        if self.status == 'present':
            return 1
        elif self.status == 'absent':
            return 0
        elif self.status == 'absent_with_reason':
            return 0.5

    def __str__(self):
        return f"Attendance - {self.student} - {self.status}"
    
    @classmethod
    def getAttendanceSummary(cls):
        return cls.objects.values('school_branch__name').annotate(
            present_count=Count(Case(When(status='present', then=1))),
            absent_count=Count(Case(When(status='absent', then=1))),
            absent_with_reason_count=Count(Case(When(status='absent_with_reason', then=1))),
        ).order_by('school_branch__name')
    

    @classmethod
    def getStudentAttendanceSummary(cls, student: object, current_session: object) -> dict:
        all_attendance = cls.objects.filter(student=student, session=current_session).select_related(
            "student", "student__user", "session", "school_branch__manager", "created_by"
        ).all()
        total_attendance = all_attendance.count()

        present_count = all_attendance.filter(status="present").count()
        absent_count = all_attendance.filter(status="absent").count()
        absent_with_reason_count = all_attendance.filter(status="absent_with_reason").count()

        # You can adjust the average calculation logic to match your requirements
        average_attendance = ((present_count + (0.5 * absent_with_reason_count)) / total_attendance) * 100 if total_attendance else 0

        # Get the reasons for absences with reason
        reasons = all_attendance.filter(status="absent_with_reason").values_list('reason_for_absence', flat=True)

        return {
            'all_attendance': all_attendance,
            'present_count': present_count,
            'absent_count': absent_count,
            'absent_with_reason_count': absent_with_reason_count,
            'average_attendance': average_attendance,
            'reasons': list(reasons)
        }
    

    @classmethod
    def getStudentsWithHighAttendance(cls, threshold: float, limit: int) -> list[object]:
    # Calculate the average attendance score for each student
        students_with_attendance = cls.objects.annotate(
            attendance_avg=Avg(
                Case(
                    # When present, count as 1
                    When(status='present', then=Value(1)),
                    # When absent, count as 0
                    When(status='absent', then=Value(0)),
                    # When absent with reason, count as 0.5
                    When(status='absent_with_reason', then=Value(0.5)),
                    output_field=FloatField()
                )
            )
        ).filter(attendance_avg__gt=threshold
        ).select_related("student__user", "student__course", "session", "school_branch__manager", "class_name__name", "created_by", "created_by")  # Filter students with attendance average > 0.7

        return students_with_attendance[:limit]
    

class TeacherAttendance(TimeStamp):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="attendance")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    school_branch = models.ForeignKey(SchoolBranch, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=40, choices=ATTENDANCE_STATUS, default="absent")
    reason_for_absence = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,
                                    limit_choices_to={'role__in': ["admin", "tech_support", "mini_tech_support", "superuser"]},
                                    related_name="teacher_attendance_taken"
                                    )

    def getTeacherAttendanceScore(self):
        if self.status == 'present':
            return 1
        elif self.status == 'absent':
            return 0
        elif self.status == 'absent_with_reason':
            return 0.5

    def __str__(self):
        return f"Attendance - {self.teacher} - {self.status}"
    

    @classmethod
    def getAttendanceSummary(cls):
        return cls.objects.values('school_branch__name').annotate(
            present_count=Count(Case(When(status='present', then=1))),
            absent_count=Count(Case(When(status='absent', then=1))),
            absent_with_reason_count=Count(Case(When(status='absent_with_reason', then=1))),
        ).order_by('school_branch__name')
    

    @classmethod
    def getTeacherAttendanceSummary(cls, teacher: object, current_session: object) -> dict:
        all_attendance = cls.objects.filter(teacher=teacher, session=current_session).select_related(
            "teacher", "teacher__user", "session", "school_branch", "created_by"
        ).all()
        total_attendance = all_attendance.count()

        present_count = all_attendance.filter(status="present").count()
        absent_count = all_attendance.filter(status="absent").count()
        absent_with_reason_count = all_attendance.filter(status="absent_with_reason").count()

        # You can adjust the average calculation logic to match your requirements
        average_attendance = ((present_count + (0.5 * absent_with_reason_count)) / total_attendance) * 100 if total_attendance else 0

        # Get the reasons for absences with reason
        reasons = all_attendance.filter(status="absent_with_reason").values_list('reason_for_absence', flat=True)

        return {
            'all_attendance': all_attendance,
            'present_count': present_count,
            'absent_count': absent_count,
            'absent_with_reason_count': absent_with_reason_count,
            'average_attendance': average_attendance,
            'reasons': list(reasons)
        }
    

    @classmethod
    def getTeachersWithHighAttendance(cls, threshold: float, limit: int) -> list[object]:
    # Calculate the average attendance score for each student
        teachers_with_attendance = cls.objects.annotate(
            attendance_avg=Avg(
                Case(
                    # When present, count as 1
                    When(status='present', then=Value(1)),
                    # When absent, count as 0
                    When(status='absent', then=Value(0)),
                    # When absent with reason, count as 0.5
                    When(status='absent_with_reason', then=Value(0.5)),
                    output_field=FloatField()
                )
            )
        ).filter(attendance_avg__gt=threshold
        ).select_related("teacher__user", "session", "school_branch__manager", "created_by",)  # Filter teachers with attendance average > 0.7

        return teachers_with_attendance[:limit]