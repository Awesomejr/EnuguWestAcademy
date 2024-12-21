import logging
import pprint
import datetime
import json
import random

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.core.paginator import Paginator

from base.forms import (CreateUserForm, ParentProfileForm, StudentProfileForm, TeacherProfileForm, 
                        StudentAttendanceSearchForm, TeacherAttendanceSearchForm,UpdateUserForm, 
                        UpdateStudentProfileForm, ManagementActionForm, UpdateTeacherProfileForm,
                        EditStudentAttendanceForm
                    )
from base.models import (ParentProfile, StudentProfile, CustomUser, TeacherProfile, 
                        Session, SchoolBranch, Subject, Topic, Class, ClassSection,
                        Course, PrevillagedUserProfile, ClassName
                    )
from examination.models import Question
from examination.models import Exam, CBTCategory
from attendance.models import StudentAttendance, TeacherAttendance
from utilities import customFuncs, customVars


logger = logging.getLogger(__name__)
CURRENT_SESSION = customFuncs.getCurrentSession(Session)


# PrevillagedUserProfile

# Create your views here.
@login_required(login_url="base:home")
def dashboard(request):
    manager_profile = request.user.previllageduserprofile
    number_to_display = 10
    school_branches = SchoolBranch.objects.all().select_related("manager")
    subjects = Subject.objects.all()
    students = customFuncs.getStudentProfiles(
                                StudentProfileModel=StudentProfile, 
                                session=CURRENT_SESSION
                            ).filter(
                                school_branch=manager_profile.school_branch
                            )
    parents = customFuncs.getParentProfiles(ParentProfileModel=ParentProfile, session=CURRENT_SESSION)
    teachers = customFuncs.getTeacherProfiles(
                                TeacherProfileModel=TeacherProfile
                            ).filter(school_branch=manager_profile.school_branch)
    exams = CBTCategory.objects.select_related(
                                        "assigned_class", "supervisor", "created_by", "session" 
                                    ).filter(
                                        session=CURRENT_SESSION,
                                        published=True
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

    context = {
        "total_school_branches": school_branches.count(), "total_subjects": subjects.count(),
        "students_preview": students[:number_to_display], "parents_preview": parents[:number_to_display],
        "students": students, "parents": parents,
        "students_in_each_branch": students_in_each_branch,
        "teachers_in_each_branch": teachers_in_each_branch,
        "branch_name": branch_name, "number_of_students": number_of_students,
        "teachers": teachers, "exams": exams, "teacher_branch_name": teacher_branch_name,
        "number_of_teachers": number_of_teachers,
    }
    return render(request, "./manager/pages/dashboard.html", context=context)


@login_required(login_url="base:home")
def registerParent(request):
    manager_profile = request.user.previllageduserprofile
    school_branch = manager_profile.school_branch

    if request.method == "POST":
        create_user_form = CreateUserForm(request.POST, request.FILES)
        parent_profile_form = ParentProfileForm(request.POST)
        if create_user_form.is_valid() and parent_profile_form.is_valid():
            logger.info(f"Create Parent Data: {create_user_form.cleaned_data}")
            logger.info(f"Parent Profile Data: {parent_profile_form.cleaned_data}")

            first_name = str(create_user_form.cleaned_data.get("first_name")).strip().capitalize()
            last_name = str(create_user_form.cleaned_data.get("last_name")).strip().capitalize()
            middle_name = str(create_user_form.cleaned_data.get("middle_name")).strip().capitalize()
            avatar = create_user_form.cleaned_data.get("avatar")
            
            parent = create_user_form.save(commit=False)
            parent.role = "parent"

            if avatar:
                try:
                    resized_avatar = customFuncs.resizeImage(avatar)
                    parent.avatar = resized_avatar
                except:
                    pass
            parent.email = customFuncs.generateUserEmail(
                                                first_name=first_name, 
                                                last_name=last_name, 
                                                middle_name=middle_name
                                            )
            parent.username = customFuncs.generateUsername(first_name=first_name, last_name=last_name)
            parent.save()

            parent_profile = ParentProfile.objects.get(user=parent)

            parent_profile.school_branch = school_branch
            parent_profile.nationality = parent_profile_form.cleaned_data.get("nationality")
            parent_profile.state = parent_profile_form.cleaned_data.get("state")
            parent_profile.local_government_area = parent_profile_form.cleaned_data.get("local_government_area")
            parent_profile.town = parent_profile_form.cleaned_data.get("town")
            parent_profile.religion = parent_profile_form.cleaned_data.get("religion")
            parent_profile.address = parent_profile_form.cleaned_data.get("address")
            parent_profile.identofication_type = parent_profile_form.cleaned_data.get("identofication_type")
            parent_profile.identofication_number = parent_profile_form.cleaned_data.get("identofication_number")
            parent_profile.father_occupation = parent_profile_form.cleaned_data.get("father_occupation")
            parent_profile.mother_occupation = parent_profile_form.cleaned_data.get("mother_occupation")
            parent_profile.father_work_address = parent_profile_form.cleaned_data.get("father_work_address")
            parent_profile.mother_work_address = parent_profile_form.cleaned_data.get("mother_work_address")
            parent_profile.phone_number = parent_profile_form.cleaned_data.get("phone_number")
            parent_profile.secondary_phone_number = parent_profile_form.cleaned_data.get("secondary_phone_number")
            parent_profile.created_by = request.user
            parent_profile.save()

            logger.info(f"Parent Profile For '{parent.getFullName}' Has Been Created.")
            messages.success(request, f"Parent Profile For '{parent.getFullName}' Has Been Created.")
            return redirect("manager:registerStudent", parentID=parent_profile.custom_user_id)
        else:
            customFuncs.displayFormErrors(request, create_user_form, messages, logger)
            customFuncs.displayFormErrors(request, parent_profile_form, messages, logger)
    else:
        create_user_form = CreateUserForm()
        parent_profile_form = ParentProfileForm(initial={"school_branch": school_branch})
    

    context = {"create_user_form": create_user_form, "parent_profile_form": parent_profile_form}
    return render(request, "manager/pages/registerParent.html", context=context)


@login_required(login_url="base:home")
def registerStudent(request, parentID):
    manager_profile = request.user.previllageduserprofile
    school_branch = manager_profile.school_branch

    parent_profile = ParentProfile.objects.select_related("user").get(custom_user_id=parentID)
    student_profile = StudentProfile.objects.select_related("user", "parent").get(parent=parent_profile)
    student = student_profile.user
    logger.debug(f"Student Profile: {student_profile}")
    logger.debug(f"Student Profile: {student_profile.parent}")

    if request.method == "POST":
        create_user_form = CreateUserForm(request.POST, request.FILES, instance=student)
        student_profile_form = StudentProfileForm(request.POST, instance=student_profile)
        if create_user_form.is_valid() and student_profile_form.is_valid():
            logger.info(f"Create Student Data: {create_user_form.cleaned_data}")
            logger.info(f"Student Profile Data: {student_profile_form.cleaned_data}")

            first_name = str(create_user_form.cleaned_data.get("first_name")).strip().capitalize()
            last_name = str(create_user_form.cleaned_data.get("last_name")).strip().capitalize()
            middle_name = str(create_user_form.cleaned_data.get("middle_name")).strip().capitalize()
            avatar = create_user_form.cleaned_data.get("avatar")

            student = create_user_form.save(commit=False)
            student.role = "student"
            if avatar:
                try:
                    resized_avatar = customFuncs.resizeImage(avatar)
                    student.avatar = resized_avatar
                except:
                    pass
            student.email = customFuncs.generateUserEmail(first_name=first_name, last_name=last_name, middle_name=middle_name)
            student.username = customFuncs.generateStudentUsername(first_name=first_name, last_name=last_name)
            student.first_name = first_name
            student.save()

            student_profile_ = student_profile_form.save(commit=False)
            student_profile_.created_by = request.user
            student_profile_.school_branch = school_branch
            student_profile_.save()

            messages.success(request, f"Student Profile For '{student.getFullName}' Has Been Created.")
            return redirect("manager:registerParent")
        else:
            customFuncs.displayFormErrors(request, create_user_form, messages, logger)
            customFuncs.displayFormErrors(request, student_profile_form, messages, logger)
    else:
        initial_data = {
            "school_branch": school_branch,
            "state": parent_profile.state,
            "nationality": parent_profile.nationality,
            "local_government_area": parent_profile.local_government_area,
            "town": parent_profile.town,
            "religion": parent_profile.religion,
            "permanent_address": parent_profile.address,
            "registration_number": customFuncs.generateStudentRegistrationNumber(
                current_session=CURRENT_SESSION,
                parent_first_name=parent_profile.user.first_name,
                parent_last_name=parent_profile.user.last_name,
            )

        }
        create_user_form = CreateUserForm(instance=student)
        student_profile_form = StudentProfileForm(instance=student_profile, initial=initial_data)

    context = {"create_user_form": create_user_form, "student_profile_form": student_profile_form, 
                "parent_profile": parent_profile
        }
    return render(request, "manager/pages/registerStudent.html", context=context)


@login_required(login_url="base:home")
def registerTeacher(request):
    manager_profile = request.user.previllageduserprofile
    school_branch = manager_profile.school_branch

    if request.method == "POST":
        create_user_form = CreateUserForm(request.POST, request.FILES)
        teacher_profile_form = TeacherProfileForm(request.POST)
        if create_user_form.is_valid() and teacher_profile_form.is_valid():
            logger.info(f"Create Teacher Data: {create_user_form.cleaned_data}")
            logger.info(f"Teacher Profile Data: {teacher_profile_form.cleaned_data}")

            first_name = str(create_user_form.cleaned_data.get("first_name")).strip().capitalize()
            last_name = str(create_user_form.cleaned_data.get("last_name")).strip().capitalize()
            middle_name = str(create_user_form.cleaned_data.get("middle_name")).strip().capitalize()
            avatar = create_user_form.cleaned_data.get("avatar")

            teacher = create_user_form.save(commit=False)
            teacher.role = "teacher"
            if avatar:
                resized_avatar = customFuncs.resizeImage(avatar)
                teacher.avatar = resized_avatar
            teacher.email = customFuncs.generateUserEmail(
                                            first_name=first_name, 
                                            last_name=last_name, 
                                            middle_name=middle_name
                                            )
            teacher.username = customFuncs.generateStudentUsername(first_name=first_name, last_name=last_name)
            teacher.save()

            teacher_profile = TeacherProfile.objects.get(user=teacher)

            teacher_profile.school_branch = school_branch
            teacher_profile.gender=teacher_profile_form.cleaned_data.get("gender")
            teacher_profile.nationality=teacher_profile_form.cleaned_data.get("nationality")
            teacher_profile.state=teacher_profile_form.cleaned_data.get("state")
            teacher_profile.local_government_area=teacher_profile_form.cleaned_data.get("local_government_area")
            teacher_profile.town=teacher_profile_form.cleaned_data.get("town")
            teacher_profile.religon=teacher_profile_form.cleaned_data.get("religion")
            teacher_profile.current_address=teacher_profile_form.cleaned_data.get("current_address")
            teacher_profile.permanent_address=teacher_profile_form.cleaned_data.get("permanent_address")
            teacher_profile.phone_number=teacher_profile_form.cleaned_data.get("phone_number")
            teacher_profile.qualification=teacher_profile_form.cleaned_data.get("qualification")
            teacher_profile.cv=teacher_profile_form.cleaned_data.get("cv")
            teacher_profile.relationship=teacher_profile_form.cleaned_data.get("relationship")
            teacher_profile.any_experience=teacher_profile_form.cleaned_data.get("any_experience")
            teacher_profile.experience_description=teacher_profile_form.cleaned_data.get("experience_description")
            teacher_profile.teacher_subject=teacher_profile_form.cleaned_data.get("teacher_subject")
            teacher_profile.teacher_status=teacher_profile_form.cleaned_data.get("teacher_status")
            teacher_profile.assigned_class.set(teacher_profile_form.cleaned_data.get("assigned_class"))
            teacher_profile.salary=teacher_profile_form.cleaned_data.get("salary")
            teacher_profile.created_by = request.user
            teacher_profile.save()

            messages.success(request, f"Teacher Profile For '{teacher.getFullName}' Has Been Created.")
            return redirect("manager:registerTeacher")
        else:
            customFuncs.displayFormErrors(request, create_user_form, messages, logger)
            customFuncs.displayFormErrors(request, teacher_profile_form, messages, logger)
    else:
        create_user_form = CreateUserForm()
        teacher_profile_form = TeacherProfileForm(initial={"school_branch": school_branch})

    context = {"create_user_form": create_user_form, "teacher_profile_form": teacher_profile_form}
    return render(request, "manager/pages/registerTeacher.html", context=context)


@login_required(login_url="base:home")
def studentsAttendance(request):
    students_to_display = None
    class_id = request.GET.get("assigned_class")
    today = customFuncs.getWeekDay()

    manager_profile = request.user.previllageduserprofile
    school_branch = manager_profile.school_branch
    
    students = customFuncs.getStudentProfiles(
                                            StudentProfileModel=StudentProfile, 
                                            session=CURRENT_SESSION
                                        ).filter(school_branch=school_branch)

    class_name = Class.objects.filter(id=class_id).first()
    
    if class_id:
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

    form = StudentAttendanceSearchForm(request.GET)

    if class_id:
        paginator = Paginator(students_to_display, int(len(students_to_display)))
    else:
        paginator = Paginator(students_to_display, int(customVars.NUMBER_OF_TABLE_ROW))
    page_number = request.GET.get("page")
    students_page =paginator.get_page(page_number)

    context = {
        "form": form,
        "students": students,
        "students_to_display": students_page,
        "class_id": class_id,
    }

    if request.htmx:
        return render(request, "./techsupport/components/studentsAttendanceTable.html", context=context)
    
    return render(request, "./manager/pages/markStudentsAttendance.html", context=context)


@login_required(login_url="base:home")
def takeStudentsAttendance(request, class_id):
    class_name = None
    manager_profile = request.user.previllageduserprofile
    school_branch = manager_profile.school_branch
    
    try:
        class_name = Class.objects.filter(id=class_id).first()
    except:
        messages.error(request, f"Filter the attendance by class.")
        return redirect("manager:studentsAttendance")
    logger.debug(f"School Branch: {school_branch}")
    logger.debug(f"Class Name: {class_name}")
    
    students = None
    student_qs = StudentProfile.objects.select_related(
                                                "classes__section", "classes__name",
                                                "school_branch__manager"
                                            ).filter(school_branch=school_branch).all()
    today = customFuncs.getWeekDay()

    if request.method == "POST":
        if today in [customVars.FRIDAY, customVars.SARTUDAY, customVars.SUNDAY, customVars.MONDAY]:
            students = student_qs.filter(classes=class_name,
                                        school_branch=school_branch,
                                    )
        else:
            students = student_qs.filter(classes=class_name,
                                        school_branch=school_branch,
                                        student_status="Full-time",
                                    )

        for index, student_profile in enumerate(students, start=1):
            status = request.POST.get(f'status_{student_profile.user.id}')
            reason = request.POST.get(f'reason_{student_profile.user.id}', "")
            logger.info(f"{index}: {student_profile.user.getFullName}- {status}: {reason} {student_profile.student_status}")
            
            StudentAttendance.objects.create(
                student=student_profile,
                class_name=student_profile.classes,
                session=CURRENT_SESSION,
                school_branch=school_branch,
                status=status,
                reason_for_absence=reason if status == 'absent_with_reason' else None,
                created_by=request.user
            )

        messages.success(request, "Attendance has been recorded.")
        return redirect('manager:studentsAttendance')
    return redirect('manager:studentsAttendance')


@login_required(login_url="base:home")
def previewStudentsMarkedAttendance(request):
    attendance_to_display = None
    redirect_link = "manager:previewStudentsMarkedAttendance"
    class_id = request.GET.get("assigned_class")
    attendance_date = request.GET.get("date")

    manager_profile = request.user.previllageduserprofile
    manager_school_branch = manager_profile.school_branch
    all_attendance = StudentAttendance.objects.select_related(
                                            "class_name__section", "created_by",
                                            "class_name__name", "session", "student__user",
                                            "student__school_branch"
                                        ).filter(
                                            session=CURRENT_SESSION, school_branch=manager_school_branch
                                        ).all().order_by("-created_on")

    class_name = Class.objects.filter(id=class_id).first()
    logger.debug(f"Class Name: {class_name}")

    if class_name and attendance_date:
        selected_date = datetime.datetime.strptime(attendance_date, "%Y-%m-%d").date()
        attendance_to_display = all_attendance.filter(
            session=CURRENT_SESSION,
            class_name=class_name, 
            school_branch=manager_school_branch, 
            date=selected_date,
        ).all()
    elif class_name:
        attendance_to_display = all_attendance.filter(
            session=CURRENT_SESSION,
            class_name=class_name, 
            school_branch=manager_school_branch, 
        ).all()
    else:
        attendance_to_display = all_attendance[:500]
    logger.debug(f"Attendance: {attendance_to_display}")
    
    if class_id:
        paginator = Paginator(attendance_to_display, 2000)
    else:
        paginator = Paginator(attendance_to_display, int(customVars.NUMBER_OF_TABLE_ROW))
    page_number = request.GET.get("page")
    attendances_page =paginator.get_page(page_number)
    
    if request.method == "POST":
        form = ManagementActionForm(request.POST, list_of_actions=customVars.DELETE_MANAGEMENT_ACTION)
        if form.is_valid():
            action = form.cleaned_data.get("action")
            selected_attendances = request.POST.getlist('selected_attendances') 
            logger.debug(f"Selected Attendance: {selected_attendances}")
            if not selected_attendances:
                messages.info(request, "Select one or more attendance to perform an action.")
                return redirect(redirect_link)
            logger.debug(f"Action: {action}")
            logger.debug(f"Selected Attendances IDs: {selected_attendances}")

            customFuncs.objectModificationLog(request, logger, "attendance(s)")
            if action == "Delete":
                StudentAttendance.objects.filter(id__in=selected_attendances).delete()
                logger.info("Selected attendances have been deleted.")
                messages.success(request, "Selected attendances have been deleted.")
                return redirect(redirect_link)

    student_attendance_search_form = StudentAttendanceSearchForm(request.GET)
    form = ManagementActionForm(list_of_actions=customVars.DELETE_MANAGEMENT_ACTION)

    context = {
        "form": form, "student_attendance_search_form": student_attendance_search_form,
        "total_attendance": all_attendance.count(),
        "attendances_to_display": attendances_page,
    }

    if request.htmx:
        return render(request, "./techsupport/components/previewStudentsMarkedAttendanceTable.html", context=context)
    
    return render(request, "./manager/pages/previewStudentsMarkedAttendance.html", context=context)


@login_required(login_url="base:home")
def studentsAttendanceStatistics(request):
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

    students_with_high_attendance = StudentAttendance.getStudentsWithHighAttendance(threshold=0.9, limit=20)

    context = {
        "branch_name_json": branch_name_json,
        "branch_count_json": branch_count_json,
        "students_with_high_attendance": students_with_high_attendance,
        "attendance_of_each_branch": attendance_of_each_branch,
        "attendance_summary": attendance_summary
    }
    return render(request, "./manager/pages/studentsAttendanceStatistics.html", context=context)


@login_required(login_url="base:home")
def editStudentAttendance(request, attendanceId):
    attendance = StudentAttendance.objects.get(id=attendanceId)

    if request.method == "POST":
        form = EditStudentAttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            attendance_obj = form.save(commit=False)
            attendance_obj.created_by = request.user
            attendance_obj = form.save()
            logger.info(f"Attendance updated successfully.")
            messages.success(request, f"Attendance updated successfully.")
            return redirect("manager:previewStudentsMarkedAttendance")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = EditStudentAttendanceForm(instance=attendance)

    context = {"form": form, "attendance": attendance}
    return render(request, "./manager/pages/editStudentAttendance.html", context=context)


@login_required(login_url="base:home")
def viewStudentAttendance(request, studentId):
    manager_profile = request.user.previllageduserprofile
    # school_branch = manager_profile.school_branch

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
    return render(request, "manager/pages/viewStudentAttendance.html", context=context)


@login_required(login_url="base:home")
def teacherAttendance(request):
    manager_profile = request.user.previllageduserprofile
    school_branch = manager_profile.school_branch
    teachers = TeacherProfile.objects.select_related(
                                        "user", "school_branch__manager", 
                                        "teacher_subject",
                                        ).all()
    all_attendance = TeacherAttendance.objects.filter(
                                                school_branch=school_branch,
                                                session=CURRENT_SESSION,
                                            ).select_related(
                                                "teacher__user", "created_by",
                                                "session", "teacher__school_branch"
                                            ).all().order_by("-created_on")
    
    teachers_to_display = None
    today = customFuncs.getWeekDay()
    logger.debug(f"Today: {today}")

    if school_branch:
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
    }


    if request.htmx:
        return render(request, "manager/components/teacherAttendanceTable.html", context=context)

    return render(request, "manager/pages/teacherAttendance.html", context=context)


@login_required(login_url="base:home")
def takeTeacherAttendance(request):
    teachers = None
    manager_profile = request.user.previllageduserprofile
    school_branch = manager_profile.school_branch
    teacher_qs = TeacherProfile.objects.select_related(
                                                "teacher_subject", "school_branch",
                                                "school_branch__manager"
                                            ).all()
    teacher_qs = customFuncs.getTeacherProfiles(TeacherProfileModel=TeacherProfile).filter(school_branch=school_branch)
    today = customFuncs.getWeekDay()
    if request.method == "POST":
        if today in [customVars.FRIDAY, customVars.SARTUDAY, customVars.SUNDAY]:
            teachers = teacher_qs.filter(school_branch=school_branch)
        else:
            teachers = teacher_qs.filter(school_branch=school_branch,
                                        teacher_status="Full-time",
                                    )

        for index, teacher_profile in enumerate(teachers, start=1):
            status = request.POST.get(f'status_{teacher_profile.user.id}')
            reason = request.POST.get(f'reason_{teacher_profile.user.id}', "")
            logger.info(f"{index}: {teacher_profile.user.getFullName}- {status}: {reason} {teacher_profile.teacher_status}")
            
            TeacherAttendance.objects.create(
                teacher=teacher_profile,
                session=CURRENT_SESSION,
                school_branch=school_branch,
                status=status,
                reason_for_absence=reason if status == 'absent_with_reason' else None,
                created_by=request.user
            )

        messages.success(request, "Attendance has been recorded.")
        return redirect('manager:teacherAttendance')
    return redirect('manager:teacherAttendance')


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
    return render(request, "manager/pages/viewTeacherAttendance.html", context=context)


@login_required(login_url="base:home")
def viewStudents(request):
    students_to_display = None
    search_input = request.GET.get("q", " ").strip()
    filter_input = request.GET.get("filter")
    class_input = request.GET.get("classId")
    redirect_link = "manager:viewStudents"

    manager_profile = request.user.previllageduserprofile
    school_branch = manager_profile.school_branch

    students = customFuncs.getStudentProfiles(
                                            StudentProfileModel=StudentProfile, 
                                            session=CURRENT_SESSION
                                        ).filter(school_branch=school_branch)

    if class_input:
        selected_class = Class.objects.get(id=class_input)
        students = students.filter(classes=selected_class)

    student_male_count = students.filter(gender="Male").count()
    student_female_count = students.filter(gender="Female").count()

    if search_input == "suspended" or search_input == "suspend":
        students_to_display = students.filter(user__is_suspended__icontains=1)
    # elif search_input == "deleted" or search_input == "delete":
    #     students_to_display = students.filter(user__is_deleted__icontains=1)
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

    
    if request.method == "POST":
        form = ManagementActionForm(request.POST, list_of_actions=customVars.MANAGEMENT_ACTIONS)
        if form.is_valid():
            action = form.cleaned_data.get("action")
            selected_students = request.POST.getlist('selected_students')  # Get selected student IDs
            if not selected_students:
                messages.info(request, "Select one or more students to perform an action.")
                return redirect(redirect_link)
            logger.debug(f"Action: {action}")
            logger.debug(f"Selected Student IDs: {selected_students}")

            customFuncs.objectModificationLog(request, logger, "student(s)")
            if action == "Delete":
                # CustomUser.objects.filter(id__in=selected_students).delete()
                CustomUser.objects.filter(id__in=selected_students).update(is_deleted=True)
                logger.info("Selected students have been deleted.")
                messages.success(request, "Selected students have been deleted.")
                return redirect(redirect_link)
            elif action == "Undelete":
                CustomUser.objects.filter(id__in=selected_students).update(is_deleted=False)
                logger.info("Selected students have been undeleted.")
                messages.success(request, "Selected students have been undeleted.")
                return redirect(redirect_link)
            elif action == "Suspend":
                CustomUser.objects.filter(id__in=selected_students).update(is_suspended=True)
                logger.info("Selected students have been suspended.")
                messages.success(request, "Selected students have been suspended.")
                return redirect(redirect_link)
            elif action == "Unsuspend":
                CustomUser.objects.filter(id__in=selected_students).update(is_suspended=False)
                logger.info("Selected students have been unsuspended.")
                messages.success(request, "Selected students have been unsuspended.")
                return redirect(redirect_link)
            elif action == "Reset-Password":
                for student_id in selected_students:
                    student = CustomUser.objects.get(id=student_id)
                    student.user.set_password(customVars.DEFAULT_PASSWORD)
                    student.user.save()
                logger.info("Passwords have been reset for the selected students.")
                messages.success(request, "Passwords have been reset for the selected students.")
                return redirect(redirect_link)
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = ManagementActionForm(list_of_actions=customVars.MANAGEMENT_ACTIONS)

    
    context = {
        "students": students_page, "form": form, 
        "students_count": students.count, "student_male_count": student_male_count,
        "student_female_count": student_female_count,
    }
    if request.htmx:
        return render(request, "techsupport/components/viewStudentsTable.html", context=context)
    return render(request, "manager/pages/viewStudents.html", context=context)


@login_required(login_url="base:home")
def editStudent(request, studentId):
    student = CustomUser.objects.filter(id=studentId).first()
    student_profile = StudentProfile.objects.filter(user=student
                                                ).select_related(
                                                    "user", "parent", "parent__session", 
                                                    "parent__user", "school_branch", 
                                                    "classes__name", "classes__section"
                                                ).first()
    student_parent = student_profile.parent

    if request.method == "POST":
        update_user_form = UpdateUserForm(request.POST, instance=student)
        update_student_profile_form = UpdateStudentProfileForm(request.POST, instance=student_profile)
        customFuncs.objectModificationLog(request, logger, "student account & profile")
        if update_user_form.is_valid() and update_student_profile_form.is_valid():
            username = update_user_form.cleaned_data.get("username")
            if username == "":
                username = customFuncs.generateStudentUsername(
                                first_name=student.first_name,
                                last_name=student.last_name
                            )
            email = update_user_form.cleaned_data.get("email")
            if email == "":
                email = customFuncs.generateUserEmail(
                                first_name=student.first_name, 
                                last_name=student.last_name, 
                                middle_name=student.middle_name
                            )
            logger.debug(f"Email: {email}")
            user_ = update_user_form.save(commit=False)
            user_.email = email
            user_.role = "student"
            user_.save()

            registration_number = update_student_profile_form.cleaned_data.get("registration_number")
            if registration_number == "":
                registration_number = customFuncs.generateStudentRegistrationNumber(
                            current_session=CURRENT_SESSION,
                            parent_first_name=student_parent.user.first_name,
                            parent_last_name=student_parent.user.last_name
                        )
            logger.debug(f"Reg Num: {registration_number}")

            profile = update_student_profile_form.save(commit=False)
            profile.registration_number = registration_number
            profile.created_by = request.user
            profile.parent = student_parent
            profile.save()

            logger.info(f"'{student.getFullName}' profile has been updated.".capitalize())
            messages.success(request, f"'{student.getFullName}' profile has been updated.".capitalize())
            return redirect("manager:viewStudents")
    else:
        update_user_form = UpdateUserForm(instance=student)
        update_student_profile_form = UpdateStudentProfileForm(instance=student_profile)

    context = {
        "student_profile": student_profile, "student": student, "update_user_form": update_user_form,
        "update_student_profile_form": update_student_profile_form, "student_parent": student_parent,
    }
    return render(request, "manager/pages/editStudent.html", context=context)


@login_required(login_url="base:home")
def viewTeachers(request):
    teachers_to_display = None
    search_input = request.GET.get("q", " ").strip()
    filter_input = request.GET.get("filter")
    class_input = request.GET.get("classId")
    redirect_link = "manager:viewTeachers"
    manager_profile = request.user.previllageduserprofile
    school_branch = manager_profile.school_branch

    teachers = customFuncs.getTeacherProfiles(TeacherProfileModel=TeacherProfile).filter(
                                                        school_branch=school_branch
                                                    )

    if class_input:
        selected_class = Class.objects.get(id=class_input)
        teachers = teachers.filter(assigned_class=selected_class)

    teacher_male_count = teachers.filter(gender="Male").count()
    teacher_female_count = teachers.filter(gender="Female").count()

    if search_input == "Suspended" or search_input == "suspended":
        teachers_to_display = teachers.filter(user__is_suspended__icontains=1)
    # elif search_input == "deleted" or search_input == "delete":
    #     teachers_to_display = customFuncs.getTeacherProfiles(
    #                         TeacherProfileModel=TeacherProfile, delete_status=0
    #                     ).filter(user__is_deleted__icontains=1)
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

    
    if request.method == "POST":
        form = ManagementActionForm(request.POST, list_of_actions=customVars.MANAGEMENT_ACTIONS)
        if form.is_valid():
            action = form.cleaned_data.get("action")
            selected_teachers = request.POST.getlist('selected_teachers')  # Get selected student IDs
            if not selected_teachers:
                messages.info(request, "Select one or more teachers to perform an action.")
                return redirect(redirect_link)
            logger.debug(f"Action: {action}")
            logger.debug(f"Selected Teacher IDs: {selected_teachers}")

            customFuncs.objectModificationLog(request, logger, "student(s)")
            if action == "Delete":
                # CustomUser.objects.filter(id__in=selected_teachers).delete()
                CustomUser.objects.filter(id__in=selected_teachers).update(is_deleted=True)
                logger.info("Selected teachers have been deleted.")
                messages.success(request, "Selected teachers have been deleted.")
                return redirect(redirect_link)
            elif action == "Undelete":
                CustomUser.objects.filter(id__in=selected_teachers).update(is_deleted=False)
                logger.info("Selected teachers have been undeleted.")
                messages.success(request, "Selected teachers have been undeleted.")
                return redirect(redirect_link)
            elif action == "Suspend":
                CustomUser.objects.filter(id__in=selected_teachers).update(is_suspended=True)
                logger.info("Selected teachers have been suspended.")
                messages.success(request, "Selected teachers have been suspended.")
                return redirect(redirect_link)
            elif action == "Unsuspend":
                CustomUser.objects.filter(id__in=selected_teachers).update(is_suspended=False)
                logger.info("Selected teachers have been unsuspended.")
                messages.success(request, "Selected teachers have been unsuspended.")
                return redirect(redirect_link)
            elif action == "Reset-Password":
                for student_id in selected_teachers:
                    student = CustomUser.objects.get(id=student_id)
                    student.user.set_password(customVars.DEFAULT_PASSWORD)
                    student.user.save()
                logger.info("Passwords have been reset for the selected teachers.")
                messages.success(request, "Passwords have been reset for the selected teachers.")
                return redirect(redirect_link)
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = ManagementActionForm(list_of_actions=customVars.MANAGEMENT_ACTIONS)

    
    context = {
        "teachers": teachers_page, "form": form, 
        "teachers_count": teachers.count, "teacher_male_count": teacher_male_count,
        "teacher_female_count": teacher_female_count
    }
    if request.htmx:
        return render(request, "techsupport/components/viewTeachersTable.html", context=context)
    return render(request, "manager/pages/viewTeachers.html", context=context)


@login_required(login_url="base:home")
def editTeacher(request, teacherId):
    manager_profile = request.user.previllageduserprofile
    school_branch = manager_profile.school_branch

    teacher = CustomUser.objects.filter(id=teacherId).first()
    teacher_profile = TeacherProfile.objects.filter(user=teacher
                                                ).select_related(
                                                    "user","school_branch", 
                                                    "created_by", "teacher_subject"
                                                ).first()

    if request.method == "POST":
        update_user_form = UpdateUserForm(request.POST, instance=teacher)
        update_teacher_profile_form = UpdateTeacherProfileForm(request.POST, instance=teacher_profile)
        customFuncs.objectModificationLog(request, logger, "teacher account & profile")
        if update_user_form.is_valid() and update_teacher_profile_form.is_valid():
            username = update_user_form.cleaned_data.get("username")
            if username == "":
                username = customFuncs.generateUsername(
                                first_name=teacher.first_name,
                                last_name=teacher.last_name
                            )
            email = update_user_form.cleaned_data.get("email")
            if email == "":
                email = customFuncs.generateUserEmail(
                                first_name=teacher.first_name, 
                                last_name=teacher.last_name, 
                                middle_name=teacher.middle_name
                            )
            logger.debug(f"Email: {email}")
            user_ = update_user_form.save(commit=False)
            user_.email = email
            user_.save()

            profile = update_teacher_profile_form.save(commit=False)
            profile.created_by = request.user
            profile.save()

            logger.info(f"'{teacher.getFullName}' profile has been updated.".capitalize())
            messages.success(request, f"'{teacher.getFullName}' profile has been updated.".capitalize())
            return redirect("manager:viewTeachers")
        else:
            customFuncs.displayFormErrors(request, update_user_form, messages, logger)
            customFuncs.displayFormErrors(request, update_teacher_profile_form, messages, logger)
    else:
        update_user_form = UpdateUserForm(instance=teacher)
        update_teacher_profile_form = UpdateTeacherProfileForm(instance=teacher_profile)

    context = {
        "teacher_profile": teacher_profile, "teacher": teacher, "update_user_form": update_user_form,
        "update_teacher_profile_form": update_teacher_profile_form
    }
    return render(request, "manager/pages/editTeacher.html", context=context)


@login_required(login_url="base:home")
def viewParents(request):
    parents_to_display = None
    search_input = request.GET.get("q", " ").strip()
    filter_input = request.GET.get("filter")
    manager_profile = request.user.previllageduserprofile
    school_branch = manager_profile.school_branch
    redirect_link = "manager:viewParents"

    parents = customFuncs.getParentProfiles(ParentProfile, session=CURRENT_SESSION).filter(school_branch=school_branch)

    if search_input == "deleted" or search_input == "delete":
        parents_to_display = customFuncs.getParentProfiles(ParentProfileModel=ParentProfile, session=CURRENT_SESSION,
                    delete_status=1).filter(user__is_deleted__icontains=1)
    elif search_input:
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

    if request.method == "POST":
        form = ManagementActionForm(request.POST, list_of_actions=customVars.MANAGEMENT_ACTIONS)
        if form.is_valid():
            action = form.cleaned_data.get("action")
            selected_parents = request.POST.getlist('selected_parents')  # Get selected parent IDs
            if not selected_parents:
                messages.info(request, "Select one or more parents to perform an action.")
                return redirect(redirect_link)
            logger.debug(f"Action: {action}")
            logger.debug(f"Selected parent IDs: {selected_parents}")

            customFuncs.objectModificationLog(request, logger, "parent(s)")
            if action == "Delete":
                # CustomUser.objects.filter(id__in=selected_parents).delete()
                CustomUser.objects.filter(id__in=selected_parents).update(is_deleted=True)
                logger.info("Selected parents have been deleted.")
                messages.success(request, "Selected parents have been deleted.")
                return redirect(redirect_link)
            elif action == "Undelete":
                CustomUser.objects.filter(id__in=selected_parents).update(is_deleted=False)
                logger.info("Selected parents have been undeleted.")
                messages.success(request, "Selected parents have been undeleted.")
                return redirect(redirect_link)
            elif action == "Suspend":
                CustomUser.objects.filter(id__in=selected_parents).update(is_suspended=True)
                logger.info("Selected parents have been suspended.")
                messages.success(request, "Selected parents have been suspended.")
                return redirect(redirect_link)
            elif action == "Unsuspend":
                CustomUser.objects.filter(id__in=selected_parents).update(is_suspended=False)
                logger.info("Selected parents have been unsuspended.")
                messages.success(request, "Selected parents have been unsuspended.")
                return redirect(redirect_link)
            elif action == "Reset-Password":
                for parent_id in selected_parents:
                    parent = CustomUser.objects.get(id=parent_id)
                    parent.user.set_password(customVars.DEFAULT_PASSWORD)
                    parent.user.save()
                logger.info("Passwords have been reset for the selected parents.")
                messages.success(request, "Passwords have been reset for the selected parents.")
                return redirect(redirect_link)
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = ManagementActionForm(list_of_actions=customVars.MANAGEMENT_ACTIONS)

    context = {
        "parents": parents_page, "form": form,
        "parents_count": parents.count,
    }

    if request.htmx:
        return render(request, "techsupport/components/viewParentsTable.html", context=context)
    return render(request, "manager/pages/viewParents.html", context=context)


@login_required(login_url="base:home")
def viewParent(request, parentId):
    parent = CustomUser.objects.get(id=parentId)
    parent_profile = parent.parentprofile
    children = parent_profile.children.all()

    context = {"parent": parent, "parent_profile": parent_profile, "children": children}
    return render(request, "./manager/pages/viewParent.html", context=context)


@login_required(login_url="base:home")
def viewQuestions(request):
    questions = Question.objects.select_related("exam", "cbt", "exam_practice", 
                                                "subject", "topic", "created_by").all()
    subjects = Subject.objects.only("name").all()
    
    filter_input = request.GET.get("filter")
    search_input = request.GET.get("q")

    if search_input:
        questions = questions.filter(
            Q(subject__name__icontains=search_input) | Q(topic__name__icontains=search_input)
        )
    elif filter_input:
        questions = questions[:int(filter_input)]
    else:
        questions = questions
    
    paginator = Paginator(questions, int(customVars.NUMBER_OF_TABLE_ROW))
    page_number = request.GET.get("page")
    questions_page =paginator.get_page(page_number)
    
    context = {"questions_to_display": questions_page, "questions": questions, "subjects": subjects}

    if request.htmx:
        return render(request, "techsupport/components/viewQuestionsTable.html", context=context)

    return render(request, "manager/pages/viewQuestions.html", context=context)