import logging
import json

from django.shortcuts import render, redirect
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from base.models import (CustomUser, StudentProfile, ParentProfile, TeacherProfile, SchoolBranch,
                        Subject, Class, ClassName, Session, Course
                        )
from base.forms import StudentAttendanceSearchForm, TeacherAttendanceSearchForm
from attendance.models import StudentAttendance, TeacherAttendance
from examination.models import (Exam, Question, StudentAnswer, Option, Result, CBTExam,
                                CBTCategory, CBTResult
                            )

from utilities import customFuncs, customVars

CURRENT_SESSION = customFuncs.getCurrentSession(Session)
logger = logging.getLogger(__name__)

# Create your views here.
@login_required(login_url="base:home")
def dashboard(request):
    number_to_display = 10
    school_branches = SchoolBranch.objects.all().select_related("manager")
    subjects = Subject.objects.all()
    students = customFuncs.getStudentProfiles(StudentProfileModel=StudentProfile, session=CURRENT_SESSION)
    teachers = TeacherProfile.objects.select_related(
                                            "user", "teacher_subject", "school_branch"
                                        )
    parents = customFuncs.getParentProfiles(ParentProfileModel=ParentProfile, session=CURRENT_SESSION)
    exams = CBTCategory.objects.select_related(
                                        "assigned_class", "supervisor", "created_by", "session" 
                                    ).all()

    # Annotate the number of students in each branch
    students_in_each_branch = (
        SchoolBranch.objects.annotate(
            branch_count=Count('studentprofile')
        )
    )
    branch_name = [branch.name for branch in students_in_each_branch]
    number_of_students = [branch.branch_count for branch in students_in_each_branch]


    # TODO
    teachers_in_each_branch = (
        SchoolBranch.objects.annotate(
            branch_count=Count("teacherprofile")
        )
    )

    teacher_branch_name = [branch.name for branch in teachers_in_each_branch]
    number_of_teachers = [branch.branch_count for branch in teachers_in_each_branch]

    context = {"total_school_branches": school_branches.count(), "total_subjects": subjects.count(),
                "students_preview": students[:number_to_display], "parents_preview": parents[:number_to_display],
                "students": students, "parents": parents,
                "students_in_each_branch": students_in_each_branch,
                "teachers_in_each_branch": teachers_in_each_branch,
                "branch_name": branch_name, "number_of_students": number_of_students,
                "teachers": teachers, "exams": exams, "teacher_branch_name": teacher_branch_name,
                "number_of_teachers": number_of_teachers,
            }
    return render(request, "./guest/pages/dashboard.html", context=context)


@login_required(login_url="base:home")
def viewInitials(request):
    context = {
        "sessions_to_display": Session.objects.all(), 
        "school_branches": SchoolBranch.objects.select_related("manager").all(),
        "all_class": Class.objects.select_related("name", "section").all().prefetch_related("subjects"),
        "courses": Course.objects.prefetch_related("subjects").all()
    }
    return render(request, "./guest/pages/viewInitials.html", context=context)


@login_required(login_url="base:home")
def studentsAttendance(request):
    students = customFuncs.getStudentProfiles(StudentProfileModel=StudentProfile, session=CURRENT_SESSION)
    all_attendance = StudentAttendance.objects.select_related(
                                            "class_name__section", "created_by",
                                            "class_name__name", "session", "student__user",
                                            "student__school_branch"
                                            ).filter(session=CURRENT_SESSION).all().order_by("-created_on")
    
    students_to_display = None
    school_branch_id = request.GET.get("school_branch")
    class_id = request.GET.get("assigned_class")
    today = customFuncs.getWeekDay()
    logger.debug(f"Today: {today}")

    school_branch = SchoolBranch.objects.filter(id=school_branch_id).first()
    class_name = Class.objects.filter(id=class_id).first()
    logger.debug(f"School Branch: {school_branch}")
    logger.debug(f"Class Name: {class_name}")
    
    if school_branch_id and class_id:
        if today in [customVars.FRIDAY, customVars.SARTUDAY, customVars.SUNDAY, customVars.MONDAY]:
            students_to_display = students.filter(
                classes=class_name, 
                school_branch=school_branch, 
            ).all()
        else:
            students_to_display = students.filter(
                classes=class_name, 
                school_branch=school_branch,
                student_status__icontains="Full-time",
            ).all()
    else:
        students_to_display = students
    
    # Get attendance count grouped by school branch
    attendance_of_each_branch = SchoolBranch.objects.annotate(
        branch_count=Count('studentattendance')
    )

    # Extract branch names and attendance counts
    branch_name = [branch.name for branch in attendance_of_each_branch]
    branch_count = [branch.branch_count for branch in attendance_of_each_branch]
    logger.debug(f"Branch Name: {branch_name}")

    # Use json.dumps to serialize the data to JSON format
    branch_name_json = json.dumps(branch_name)
    branch_count_json = json.dumps(branch_count)

    # Attendance summary
    attendance_summary = StudentAttendance.getAttendanceSummary()
    logger.debug(f"Attendance Summary: {attendance_summary}")

    students_with_high_attendance = StudentAttendance.getStudentsWithHighAttendance(threshold=0.9, limit=1000)

    form = StudentAttendanceSearchForm(request.GET)

    paginator = Paginator(students_to_display, int(customVars.NUMBER_OF_TABLE_ROW))
    page_number = request.GET.get("page")
    students_page =paginator.get_page(page_number)

    context = {
        "form": form,
        "students": students,
        "students_to_display": students_page,
        "total_attendance": all_attendance.count(),
        "attendances_to_display": all_attendance[:100],  # Limiting to 100 records
        "school_branch_id": school_branch_id,
        "branch_name_json": branch_name_json,
        "branch_count_json": branch_count_json,
        "class_id": class_id,
        "students_with_high_attendance": students_with_high_attendance,
        "attendance_of_each_branch": attendance_of_each_branch,
        "attendance_summary": attendance_summary
    }

    # Check for HTMX request and render the appropriate partial or full template
    if request.htmx:
        return render(request, "guest/components/studentsAttendanceTable.html", context=context)
    return render(request, "./guest/pages/studentsAttendance.html", context=context)


@login_required(login_url="base:home")
def viewStudentAttendance(request, studentId):
    student_profile = StudentProfile.objects.select_related(
                                        "parent", "parent__user", "session", "classes", "course", "user"
                                    ).get(custom_user_id=studentId)
    student = student_profile.user
    student_class = student_profile.classes
    class_participants = StudentProfile.objects.select_related(
                                        "parent", "parent__user", "session", "classes", "course", "user"
                                    ).filter(
                                        classes=student_class, 
                                        session=student_profile.session,
                                        school_branch=student_profile.school_branch,
                                    ).all()
    male_count = class_participants.filter(gender="Male").count()
    female_count = class_participants.filter(gender="Female").count()

    class_teachers = student_profile.classes.teachers.all() 
    student_teachers = [teacher for teacher in class_teachers if teacher.school_branch == student_profile.school_branch]


    student_attendance_summary = StudentAttendance.getStudentAttendanceSummary(student=student_profile,
                                                                                current_session=CURRENT_SESSION
                                                                            )
    student_attendance = StudentAttendance.objects.filter(student=student_profile).order_by("date")
    # Prepare the data for the chart
    dates = [attendance.date.strftime("%Y-%m-%d") for attendance in student_attendance]
    statuses = [attendance.status for attendance in student_attendance]

    # Map statuses to numerical values for plotting
    status_mapping = {
        'present': 1,
        'absent': 0,
        'absent_with_reason': 0.5
    }
    status_values = [status_mapping[status] for status in statuses]

    context = {
            "student": student, 
            "student_profile": student_profile,
            "male_count": male_count, "female_count": female_count,
            "class_participants": class_participants,
            "student_attendance_summary": student_attendance_summary,
            "student_attendance": student_attendance,
            "dates": json.dumps(dates),  # Convert Python list to JSON string,
            "status_values": json.dumps(status_values),  # Convert Python list to JSON string
            "teachers": student_teachers,
        }
    return render(request, "guest/pages/viewStudentAttendance.html", context=context)


@login_required(login_url="base:home")
def viewStudents(request):
    students_to_display = None
    search_input = request.GET.get("q", " ").strip()
    filter_input = request.GET.get("filter")
    class_input = request.GET.get("classId")

    school_branches = SchoolBranch.objects.only("name").all()
    branch_names = [branch.name for branch in school_branches]
    logger.debug(f"Branches: {branch_names}")

    students = customFuncs.getStudentProfiles(StudentProfileModel=StudentProfile, session=CURRENT_SESSION)
    logger.debug(f"Students: {students}")

    if class_input:
        selected_class = Class.objects.get(id=class_input)
        students = students.filter(classes=selected_class)

    student_male_count = students.filter(gender="Male").count()
    student_female_count = students.filter(gender="Female").count()

    if search_input == "Suspended" or search_input == "suspended":
        students_to_display = students.filter(user__is_suspended__icontains=1)
    elif search_input == "deleted" or search_input == "delete":
        students_to_display = students.filter(user__is_deleted__icontains=1)
    elif search_input:
        students_to_display = students.filter(
            Q(user__username__icontains=search_input) | Q(user__email__icontains=search_input) |
            Q(school_branch__name__icontains=search_input) | Q(registration_number__icontains=search_input) |
            Q(student_status__icontains=search_input) | Q(school_branch__name__icontains=search_input) |
            Q(user__first_name__icontains=search_input) | Q(user__last_name__icontains=search_input) |
            Q(user__last_name__icontains=search_input)
        )
    elif filter_input:
        students_to_display = students[:int(filter_input)]
    else:
        students_to_display = students

    
    paginator = Paginator(students_to_display, int(customVars.NUMBER_OF_TABLE_ROW)) # Paginate the students queryset
    page_number = request.GET.get("page")
    students_page =paginator.get_page(page_number)

    context = {
        "students": students_page, "students_count": students.count, 
        "student_male_count": student_male_count, "student_female_count": student_female_count, 
        "school_branches": school_branches,
    }

    if request.htmx:
        return render(request, "techsupport/components/viewStudentsTable.html", context=context)

    return render(request, "guest/pages/viewStudents.html", context=context)


@login_required(login_url="base:home")
def teacherAttendance(request):
    teachers = TeacherProfile.objects.select_related(
                                        "user", "school_branch__manager", 
                                        "teacher_subject",
                                        ).all()
    all_attendance = TeacherAttendance.objects.select_related(
                                            "teacher__user", "created_by",
                                            "session", "teacher__school_branch"
                                            ).all().order_by("-created_on")
    
    teachers_to_display = None
    today = customFuncs.getWeekDay()
    school_branch_id = request.GET.get("school_branch")
    school_branch = SchoolBranch.objects.filter(id=school_branch_id).select_related("manager").first()
    logger.debug(f"Today: {today}")

    if school_branch_id:
        if today in [customVars.FRIDAY, customVars.SARTUDAY, customVars.SUNDAY]:
            teachers_to_display = teachers.filter(school_branch=school_branch).all()
        else:
            teachers_to_display = teachers.filter(school_branch=school_branch,
                                                teacher_status__icontains="Full-time" 
                                                ).all()
    else:
        teachers_to_display = teachers
    
    # Get attendance count grouped by school branch
    attendance_of_each_branch = SchoolBranch.objects.annotate(
        branch_count=Count('teacherattendance')
    )

    # Extract branch names and attendance counts
    branch_name = [branch.name for branch in attendance_of_each_branch]
    branch_count = [branch.branch_count for branch in attendance_of_each_branch]
    logger.debug(f"Branch Name: {branch_name}")

    # Use json.dumps to serialize the data to JSON format
    branch_name_json = json.dumps(branch_name)
    branch_count_json = json.dumps(branch_count)

    # Attendance summary
    attendance_summary = TeacherAttendance.getAttendanceSummary()
    logger.debug(f"Attendance Summary: {attendance_summary}")

    teachers_with_high_attendance = TeacherAttendance.getTeachersWithHighAttendance(threshold=0.9, limit=20)

    form = TeacherAttendanceSearchForm(request.GET)

    context = {
        "form": form,
        "teachers_to_display": teachers_to_display,
        "attendances_to_display": all_attendance[:100],
        "attendance_summary": attendance_summary,
        "teachers_with_high_attendance": teachers_with_high_attendance,
        "branch_name_json": branch_name_json, "branch_count_json": branch_count_json,
        "school_branch_id": school_branch_id,
    }


    if request.htmx:
        return render(request, "guest/components/teacherAttendanceTable.html", context=context)

    return render(request, "guest/pages/teacherAttendance.html", context=context)


@login_required(login_url="base:home")
def viewTeacherAttendance(request, teacherId):
    teacher = CustomUser.objects.get(id=teacherId)
    teacher_profile = teacher.teacherprofile

    teacher_classes = [ assigned_class.name.name  for assigned_class in teacher_profile.assigned_class.all() ]
    logger.debug(f"Classes: {teacher_classes}")

    class_participants = StudentProfile.objects.select_related(
                                        "parent", "parent__user", "session", "classes", "course", "user"
                                    ).filter(
                                        classes__name__name__in=teacher_classes,
                                        school_branch=teacher_profile.school_branch
                                    ).order_by("school_branch", "classes")

    teacher_attendance_summary = TeacherAttendance.getTeacherAttendanceSummary(teacher=teacher_profile,
                                                                                current_session=CURRENT_SESSION
                                                                            )
    teacher_attendance = TeacherAttendance.objects.filter(teacher=teacher_profile).order_by("date")

    # Prepare the data for the chart
    dates = [attendance.date.strftime("%Y-%m-%d") for attendance in teacher_attendance]
    statuses = [attendance.status for attendance in teacher_attendance]

    # Map statuses to numerical values for plotting
    status_mapping = {
        'present': 1,
        'absent': 0,
        'absent_with_reason': 0.5
    }
    status_values = [status_mapping[status] for status in statuses]

    context = {
            "teacher": teacher, "teacher_profile": teacher_profile,
            "teacher_attendance_summary": teacher_attendance_summary,
            "teacher_attendance": teacher_attendance,
            "dates": json.dumps(dates),  # Convert Python list to JSON string,
            "status_values": json.dumps(status_values),  # Convert Python list to JSON string
            "class_participants": class_participants,
        }
    return render(request, "guest/pages/viewTeacherAttendance.html", context=context)


@login_required(login_url="base:home")
def viewParents(request):
    parents_to_display = None
    search_input = request.GET.get("q", " ").strip()
    filter_input = request.GET.get("filter")
    redirect_link = "guest:viewParents"

    parents = customFuncs.getParentProfiles(ParentProfile, session=CURRENT_SESSION)

    if search_input:
        parents_to_display = parents.filter(
            Q(user__username__icontains=search_input) | Q(user__email__icontains=search_input) |
            Q(user__first_name__icontains=search_input) | Q(user__last_name__icontains=search_input) |
            Q(phone_number__icontains=search_input) | Q(user__first_name__icontains=search_input) | 
            Q(user__last_name__icontains=search_input) | Q(user__last_name__icontains=search_input)
        )
    elif filter_input == "all":
        parents_to_display = parents
    elif filter_input:
        parents_to_display = parents[:int(filter_input)]
    else:
        parents_to_display = parents
    
    paginator = Paginator(parents_to_display, int(filter_input or customVars.NUMBER_OF_TABLE_ROW)) # Paginate the parents queryset
    page_number = request.GET.get("page")
    parents_page =paginator.get_page(page_number)


    context = {
        "parents": parents_page,
        "parents_count": parents.count,
    }

    if request.htmx:
        return render(request, "guest/components/viewParentsTable.html", context=context)
    return render(request, "guest/pages/viewParents.html", context=context)


@login_required(login_url="base:home")
def viewTeachers(request):
    teachers_to_display = None
    search_input = request.GET.get("q", " ").strip()
    filter_input = request.GET.get("filter")
    class_input = request.GET.get("classId")
    redirect_link = "guest:viewTeachers"

    school_branches = SchoolBranch.objects.only("name").all()
    branch_names = [branch.name for branch in school_branches]
    logger.debug(f"Branches: {branch_names}")

    teachers = customFuncs.getTeacherProfiles(TeacherProfileModel=TeacherProfile)

    if class_input:
        selected_class = Class.objects.get(id=class_input)
        teachers = teachers.filter(assigned_class=selected_class)

    teacher_male_count = teachers.filter(gender="Male").count()
    teacher_female_count = teachers.filter(gender="Female").count()

    if search_input == "Suspended" or search_input == "suspended":
        teachers_to_display = teachers.filter(user__is_suspended__icontains=1)
    elif search_input == "deleted" or search_input == "delete":
        teachers_to_display = customFuncs.getTeacherProfiles(
                            TeacherProfileModel=TeacherProfile, delete_status=0
                        ).filter(user__is_deleted__icontains=1)
    elif search_input:
        teachers_to_display = teachers.filter(
            Q(user__username__icontains=search_input) | Q(user__email__icontains=search_input) |
            Q(school_branch__name__icontains=search_input) | Q(teacher_subject__name__icontains=search_input) |
            Q(teacher_status__icontains=search_input) | Q(school_branch__name__icontains=search_input) |
            Q(user__first_name__icontains=search_input) | Q(user__last_name__icontains=search_input) |
            Q(user__last_name__icontains=search_input)
        )
    elif filter_input:
        teachers_to_display = teachers[:int(filter_input)]
    else:
        teachers_to_display = teachers

    
    paginator = Paginator(teachers_to_display, int(customVars.NUMBER_OF_TABLE_ROW)) # Paginate the students queryset
    page_number = request.GET.get("page")
    teachers_page =paginator.get_page(page_number)

    
    context = {
        "teachers": teachers_page,
        "teachers_count": teachers.count, "teacher_male_count": teacher_male_count,
        "teacher_female_count": teacher_female_count, "school_branches": branch_names,
    }
    if request.htmx:
        return render(request, "techsupport/components/viewTeachersTable.html", context=context)
    return render(request, "guest/pages/viewTeachers.html", context=context)