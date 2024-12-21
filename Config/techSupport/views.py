import logging
import pprint
import datetime
import json
import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.forms import modelformset_factory

from .forms import CreateQuestionForm, OptionFormSet, EditQuestionForm
from base.forms import (CreateUserForm, ParentProfileForm, StudentProfileForm, TeacherProfileForm, 
                        StudentAttendanceSearchForm, TeacherAttendanceSearchForm,
                        PrevillagedUserProfileForm, UpdateUserForm, UpdateStudentProfileForm,
                        CreateClassForm, EditClassForm, CreateTopicForm, CreateSchoolBranchForm, CreateSessionForm,
                        CreateSubjectForm, ManagementActionForm, CreateCourseForm, UpdateTeacherProfileForm,
                        EditStudentAttendanceForm
                    )
from base.models import (ParentProfile, StudentProfile, CustomUser, TeacherProfile, 
                        Session, SchoolBranch, Subject, Topic, Class, ClassSection,
                        Course, PrevillagedUserProfile, ClassName
                    )
from examination.models import Exam, Question, Option, CBTCategory, CBTExam
from attendance.models import StudentAttendance, TeacherAttendance
from utilities import customFuncs, customVars
from utilities.testData import testData


logger = logging.getLogger(__name__)
CURRENT_SESSION = customFuncs.getCurrentSession(Session)

# Create your views here.
@login_required(login_url="base:home")
def dashboard(request):
    number_to_display = 10
    school_branches = SchoolBranch.objects.all().select_related("manager")
    subjects = Subject.objects.all()
    students = customFuncs.getStudentProfiles(StudentProfileModel=StudentProfile, session=CURRENT_SESSION)
    parents = customFuncs.getParentProfiles(ParentProfileModel=ParentProfile, session=CURRENT_SESSION)
    teachers = customFuncs.getTeacherProfiles(TeacherProfileModel=TeacherProfile)
    exams = CBTCategory.objects.select_related(
                                        "assigned_class", "supervisor", "created_by", "session" 
                                    ).filter(published=True).all()

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
    
    # testData.generateParentStudentTestData(
    #     UserModel=CustomUser, ParentModel=ParentProfile, StudentModel=StudentProfile,
    #     current_session=CURRENT_SESSION, student_class="Science-Tech", student_course="Engineering", number=20
    # )
    # testData.generateParentStudentTestData(
    #     UserModel=CustomUser, ParentModel=ParentProfile, StudentModel=StudentProfile,
    #     current_session=CURRENT_SESSION, student_class="Science-Tech", student_course="Computer-Science", number=20
    # )
    # testData.generateParentStudentTestData(
    #     UserModel=CustomUser, ParentModel=ParentProfile, StudentModel=StudentProfile,
    #     current_session=CURRENT_SESSION, student_class="Science-Tech", student_course="Building-Tech", number=20
    # )

    # testData.generateParentStudentTestData(
    #     UserModel=CustomUser, ParentModel=ParentProfile, StudentModel=StudentProfile,
    #     current_session=CURRENT_SESSION, student_class="Science-Health", student_course="Medicine", number=23
    # )
    # testData.generateParentStudentTestData(
    #     UserModel=CustomUser, ParentModel=ParentProfile, StudentModel=StudentProfile,
    #     current_session=CURRENT_SESSION, student_class="Science-Health", student_course="Science-Laboratory", number=22
    # )

    # testData.generateParentStudentTestData(
    #     UserModel=CustomUser, ParentModel=ParentProfile, StudentModel=StudentProfile,
    #     current_session=CURRENT_SESSION, student_class="Commercial", student_course="Accounting", number=26
    # )
    # testData.generateParentStudentTestData(
    #     UserModel=CustomUser, ParentModel=ParentProfile, StudentModel=StudentProfile,
    #     current_session=CURRENT_SESSION, student_class="Humanities", student_course="Administration", number=24
    # )


    # testData.studentClassAttendance(Model=StudentAttendance, students=students, 
    #                                 current_session=CURRENT_SESSION, created_by=request.user
    #                             )


    # testData.generateTeacher(UserModel=CustomUser, TeacherModel=TeacherProfile, number=60)


    # testData.generateTopics(TopicModel=Topic, request=request, number=400)
    # testData.generateQuestions(request, number_of_questions_per_subject=150, single_subject=True, subject_name="English Language")


    # testData.generateExamination(ExamModel=Exam, request=request, 
    #                             current_session=CURRENT_SESSION, exam_class="Commercial"
    #                             )
    # testData.generateExamination(ExamModel=Exam, request=request, 
    #                             current_session=CURRENT_SESSION, exam_class="Humanity"
    #                             )
    # testData.generateExamination(ExamModel=Exam, request=request, 
    #                             current_session=CURRENT_SESSION, exam_class="Science-Health"
    #                             )
    # testData.generateExamination(ExamModel=Exam, request=request, 
    #                             current_session=CURRENT_SESSION, exam_class="Science-Tech"
    #                             )

    # logger.debug(f"Exams: {Exam.objects.all().delete()}")
    # Exam.objects.all().delete()
    # Question.objects.all().delete()

    # testData.generateExamQuestion(request=request)

    context = {"total_school_branches": school_branches.count(), "total_subjects": subjects.count(),
                "students_preview": students[:number_to_display], "parents_preview": parents[:number_to_display],
                "students": students, "parents": parents,
                "students_in_each_branch": students_in_each_branch,
                "teachers_in_each_branch": teachers_in_each_branch,
                "branch_name": branch_name, "number_of_students": number_of_students,
                "teachers": teachers, "exams": exams, "teacher_branch_name": teacher_branch_name,
                "number_of_teachers": number_of_teachers,
            }
    return render(request, "techsupport/pages/dashboard.html", context=context)


@login_required(login_url="base:home")
def registerParent(request):
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
            return redirect("techsupport:registerStudent", parentID=parent_profile.custom_user_id)
        else:
            customFuncs.displayFormErrors(request, create_user_form, messages, logger)
            customFuncs.displayFormErrors(request, parent_profile_form, messages, logger)
    else:
        create_user_form = CreateUserForm()
        parent_profile_form = ParentProfileForm()
    

    context = {"create_user_form": create_user_form, "parent_profile_form": parent_profile_form}
    return render(request, "techsupport/pages/registerParent.html", context=context)


@login_required(login_url="base:home")
def registerStudent(request, parentID):
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
            student.save()

            student_profile_ = student_profile_form.save(commit=False)
            student_profile_.created_by = request.user
            student_profile_.parent = parent_profile
            student_profile_.save()

            messages.success(request, f"Student Profile For '{student.getFullName}' Has Been Created.")
            return redirect("techsupport:registerParent")
        else:
            customFuncs.displayFormErrors(request, create_user_form, messages, logger)
            customFuncs.displayFormErrors(request, student_profile_form, messages, logger)
    else:
        initial_data = {
            "school_branch": parent_profile.school_branch,
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

    context = {
        "create_user_form": create_user_form, 
        "student_profile_form": student_profile_form,
        "parent_profile": parent_profile
    }
    return render(request, "techsupport/pages/registerStudent.html", context=context)


@login_required(login_url="base:home")
def registerTeacher(request):
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

            teacher_profile.date_of_birth=teacher_profile_form.cleaned_data.get("date_of_birth")
            teacher_profile.gender=teacher_profile_form.cleaned_data.get("gender")
            teacher_profile.nationality=teacher_profile_form.cleaned_data.get("nationality")
            teacher_profile.state=teacher_profile_form.cleaned_data.get("state")
            teacher_profile.local_government_area=teacher_profile_form.cleaned_data.get("local_government_area")
            teacher_profile.town=teacher_profile_form.cleaned_data.get("town")
            teacher_profile.religon=teacher_profile_form.cleaned_data.get("religion")
            teacher_profile.school_branch=teacher_profile_form.cleaned_data.get('school_branch')
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
            return redirect("techsupport:registerTeacher")
        else:
            customFuncs.displayFormErrors(request, create_user_form, messages, logger)
            customFuncs.displayFormErrors(request, teacher_profile_form, messages, logger)
    else:
        create_user_form = CreateUserForm()
        teacher_profile_form = TeacherProfileForm()

    context = {"create_user_form": create_user_form, "teacher_profile_form": teacher_profile_form}
    return render(request, "techsupport/pages/registerTeacher.html", context=context)


@login_required(login_url="base:home")
def registerPrevillagedUser(request):
    previllaged_users_profiles = PrevillagedUserProfile.objects.select_related("user").all()

    if request.method == "POST":
        create_user_form = CreateUserForm(request.POST, request.FILES)
        previllaged_user_profile_form = PrevillagedUserProfileForm(request.POST)

        if create_user_form.is_valid() and previllaged_user_profile_form.is_valid():
            role = previllaged_user_profile_form.cleaned_data.get("role")
            logger.debug(f"Role: {role}")
            first_name = str(create_user_form.cleaned_data.get("first_name")).strip().capitalize()
            last_name = str(create_user_form.cleaned_data.get("last_name")).strip().capitalize()
            middle_name = str(create_user_form.cleaned_data.get("middle_name")).strip().capitalize()
            avatar = create_user_form.cleaned_data.get("avatar")

            user = create_user_form.save(commit=False)
            user.role = role
            if avatar:
                resized_avatar = customFuncs.resizeImage(avatar)
                user.avatar = resized_avatar
            user.email = customFuncs.generateUserEmail(
                                                first_name=first_name, 
                                                last_name=last_name, 
                                                middle_name=middle_name
                                            )
            user.username = customFuncs.generateUsername(first_name=first_name, last_name=last_name)
            user.save()

            logger.info(f"Previllaged User Account For '{user.getFullName}' Has Been Created.")

            previllaged_user_profile = PrevillagedUserProfile.objects.get(user=user)
            previllaged_user_profile.nationality = previllaged_user_profile_form.cleaned_data.get("nationality")
            previllaged_user_profile.state = previllaged_user_profile_form.cleaned_data.get("state")
            previllaged_user_profile.gender = previllaged_user_profile_form.cleaned_data.get("gender")
            previllaged_user_profile.school_branch = previllaged_user_profile_form.cleaned_data.get("school_branch")
            previllaged_user_profile.local_government_area = previllaged_user_profile_form.cleaned_data.get("local_government_area")
            previllaged_user_profile.town = previllaged_user_profile_form.cleaned_data.get("town")
            previllaged_user_profile.religion = previllaged_user_profile_form.cleaned_data.get("religion")
            previllaged_user_profile.relationship = previllaged_user_profile_form.cleaned_data.get("relationship")
            previllaged_user_profile.address = previllaged_user_profile_form.cleaned_data.get("address")
            previllaged_user_profile.phone_number = previllaged_user_profile_form.cleaned_data.get("phone_number")
            previllaged_user_profile.created_by = request.user
            previllaged_user_profile.save()

            logger.info(f"User Profile For '{user.getFullName}' Has Been Created.")
            messages.success(request, f"User Profile For '{user.getFullName}' Has Been Created.")
            return redirect("techsupport:registerPrevillagedUser")
        else:
            customFuncs.displayFormErrors(request, create_user_form, messages, logger)
            customFuncs.displayFormErrors(request, previllaged_user_profile_form, messages, logger)
    else:
        create_user_form = CreateUserForm()
        previllaged_user_profile_form = PrevillagedUserProfileForm()

    context = {"create_user_form": create_user_form, "previllaged_user_profile_form": previllaged_user_profile_form, "previllaged_users_profiles": previllaged_users_profiles}
    return render(request, "techsupport/pages/registerPrevillagedUser.html", context=context)


@login_required(login_url="base:home")
def viewCustomUsers(request):
    users_to_display = None
    search_input = request.GET.get("q", " ").strip().lower()
    filter_input = request.GET.get("filter")
    redirect_link = "techsupport:viewCustomUsers"

    custom_users = CustomUser.objects.all()
    current_month = datetime.datetime.today().month
    logger.debug(f"Month: {current_month}")

    if search_input == "suspended" or search_input == "suspend":
        users_to_display = custom_users.filter(is_suspended__icontains=1)
    elif search_input == "deleted" or search_input == "delete":
        users_to_display = custom_users.filter(is_deleted=1)
    elif search_input == "active":
        users_to_display = custom_users.filter(is_active=1)
    elif search_input == "staff":
        users_to_display = custom_users.filter(is_staff=1)
    elif search_input:
        users_to_display = custom_users.filter(
            Q(username__icontains=search_input) | Q(email__icontains=search_input) |
            Q(first_name__icontains=search_input) | Q(last_name__icontains=search_input) |
            Q(last_name__icontains=search_input) | Q(role__icontains=search_input)
        )
    elif filter_input:
        users_to_display = custom_users[:int(filter_input)]
    else:
        users_to_display = custom_users


    paginator = Paginator(users_to_display, filter_input or 200) # Paginate the users queryset
    page_number = request.GET.get("page")
    custom_users_page =paginator.get_page(page_number)

    if request.method == "POST":
        form = ManagementActionForm(request.POST, list_of_actions=customVars.ADMIN_MANAGEMENT_ACTIONS)
        if form.is_valid():
            action = form.cleaned_data.get("action")
            selected_custom_users = request.POST.getlist('selected_custom_users')  # Get selected user IDs
            if not selected_custom_users:
                messages.info(request, "Select one or more users to perform an action.")
                return redirect(redirect_link)
            logger.debug(f"Action: {action}")
            logger.debug(f"Selected Users IDs: {selected_custom_users}")

            customFuncs.objectModificationLog(request, logger, "user(s)")
            if action == "Delete":
                CustomUser.objects.filter(id__in=selected_custom_users).update(is_deleted=True)
                logger.info("Selected users have been deleted.")
                messages.success(request, "Selected users have been deleted.")
                return redirect(redirect_link)
            elif action == "Undelete":
                CustomUser.objects.filter(id__in=selected_custom_users).update(is_deleted=False)
                logger.info("Selected users have been undeleted.")
                messages.success(request, "Selected users have been undeleted.")
                return redirect(redirect_link)
            elif action == "Suspend":
                CustomUser.objects.filter(id__in=selected_custom_users).update(is_suspended=True)
                logger.info("Selected users have been suspended.")
                messages.success(request, "Selected users have been suspended.")
                return redirect(redirect_link)
            elif action == "Unsuspend":
                CustomUser.objects.filter(id__in=selected_custom_users).update(is_suspended=False)
                logger.info("Selected users have been unsuspended.")
                messages.success(request, "Selected users have been unsuspended.")
                return redirect(redirect_link)
            elif action == "Staff":
                CustomUser.objects.filter(id__in=selected_custom_users).update(is_staff=True)
                logger.info("Selected users have been made a staff.")
                messages.success(request, "Selected users have been made a staff.")
                return redirect(redirect_link)
            elif action == "Unstaff":
                CustomUser.objects.filter(id__in=selected_custom_users).update(is_staff=False)
                logger.info("Selected users have been un-staffed.")
                messages.success(request, "Selected users have been un-staffed.")
                return redirect(redirect_link)
            elif action == "Active":
                CustomUser.objects.filter(id__in=selected_custom_users).update(is_active=True)
                logger.info("Selected users have been made active.")
                messages.success(request, "Selected users have been made active.")
                return redirect(redirect_link)
            elif action == "Deactive":
                CustomUser.objects.filter(id__in=selected_custom_users).update(is_active=False)
                logger.info("Selected users have been de-actived.")
                messages.success(request, "Selected users have been de-actived.")
                return redirect(redirect_link)
            elif action == "Reset-Password":
                for user_id in selected_custom_users:
                    custom_user = CustomUser.objects.get(id=user_id)
                    custom_user.set_password(customVars.DEFAULT_PASSWORD)
                    custom_user.save()
                logger.info("Passwords have been reset for the selected users.")
                messages.success(request, "Passwords have been reset for the selected users.")
                return redirect(redirect_link)
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = ManagementActionForm(list_of_actions=customVars.ADMIN_MANAGEMENT_ACTIONS)


    context = {
        "form": form,
        "custom_users": custom_users_page, 
        "custom_users_count": custom_users.count
    }

    if request.htmx:
        return render(request, "techsupport/components/viewCustomUsersTable.html", context=context)
    return render(request, "techsupport/pages/viewCustomUsers.html", context=context)


@login_required(login_url="base:home")
def studentsAttendance(request):
    students_to_display = None
    school_branch_id = request.GET.get("school_branch")
    class_id = request.GET.get("assigned_class")
    today = customFuncs.getWeekDay()
    logger.debug(f"Today: {today}")
    students = customFuncs.getStudentProfiles(StudentProfileModel=StudentProfile, session=CURRENT_SESSION)

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

    form = StudentAttendanceSearchForm(request.GET)

    if school_branch_id and class_id:
        paginator = Paginator(students_to_display, int(len(students_to_display)))
    else:
        paginator = Paginator(students_to_display, int(customVars.NUMBER_OF_TABLE_ROW))
    page_number = request.GET.get("page")
    students_page =paginator.get_page(page_number)

    context = {
        "form": form,
        "students": students,
        "students_to_display": students_page,
        "school_branch_id": school_branch_id,
        "class_id": class_id,
    }

    # Check for HTMX request and render the appropriate partial or full template
    if request.htmx:
        return render(request, "techsupport/components/studentsAttendanceTable.html", context=context)
    
    # Render full page if not an HTMX request
    return render(request, "techsupport/pages/markStudentsAttendance.html", context=context)


@login_required(login_url="base:home")
def takeStudentsAttendance(request, school_branch_id, class_id):
    school_branch = None
    class_name = None
    try:
        school_branch = SchoolBranch.objects.filter(id=school_branch_id).first()
        class_name = Class.objects.filter(id=class_id).first()
        logger.debug(f"School Branch: {school_branch}")
        logger.debug(f"Class Name: {class_name}")
    except:
        messages.error(request, f"Filter the attendance by class.")
        return redirect("techsupport:studentsAttendance")
    
    students = None
    student_qs = StudentProfile.objects.select_related(
                                                "classes__section", "classes__name",
                                                "school_branch__manager"
                                            ).all()
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
        return redirect('techsupport:studentsAttendance')
    return redirect('techsupport:studentsAttendance')


@login_required(login_url="base:home")
def previewStudentsMarkedAttendance(request):
    attendance_to_display = None
    redirect_link = "techsupport:previewStudentsMarkedAttendance"
    school_branch_id = request.GET.get("school_branch")
    class_id = request.GET.get("assigned_class")
    attendance_date = request.GET.get("date")

    all_attendance = StudentAttendance.objects.select_related(
                                            "class_name__section", "created_by",
                                            "class_name__name", "session", "student__user",
                                            "student__school_branch"
                                        ).filter(session=CURRENT_SESSION).all().order_by("-created_on")

    school_branch = SchoolBranch.objects.filter(id=school_branch_id).first()
    class_name = Class.objects.filter(id=class_id).first()

    logger.debug(f"School Branch: {school_branch}")
    logger.debug(f"Class Name: {class_name}")

    if school_branch and class_name and attendance_date:
        selected_date = datetime.datetime.strptime(attendance_date, "%Y-%m-%d").date()
        attendance_to_display = all_attendance.filter(
            session=CURRENT_SESSION,
            class_name=class_name, 
            school_branch=school_branch, 
            date=selected_date,
        ).all()
    elif school_branch and class_name:
        attendance_to_display = all_attendance.filter(
            session=CURRENT_SESSION,
            class_name=class_name, 
            school_branch=school_branch, 
        ).all()
    else:
        attendance_to_display = all_attendance[:500]
    logger.debug(f"Attendance: {attendance_to_display}")
    
    if school_branch and class_name:
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

    return render(request, "./techsupport/pages/previewStudentsMarkedAttendance.html", context=context)


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
    return render(request, "./techsupport/pages/studentsAttendanceStatistics.html", context=context)


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
            return redirect("techsupport:previewStudentsMarkedAttendance")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = EditStudentAttendanceForm(instance=attendance)

    context = {"form": form, "attendance": attendance}
    return render(request, "./techsupport/pages/editStudentAttendance.html", context=context)


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

    try:
        class_teachers = student_profile.classes.teachers.all() 
        student_teachers = [teacher for teacher in class_teachers if teacher.school_branch == student_profile.school_branch]
    except AttributeError:
        logger.error(f"Opps.. An error occured. The selected student has an imcomplete profile.")
        messages.error(
            request, f"Opps.. An error occured. \nThe selected student has an imcomplete profile. \nClick the'Edit' button to complete the student's profile."
        )
        return redirect("techsupport:viewStudents")

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
    return render(request, "techsupport/pages/viewStudentAttendance.html", context=context)


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
        return render(request, "techsupport/components/teacherAttendanceTable.html", context=context)

    return render(request, "techsupport/pages/teacherAttendance.html", context=context)


@login_required(login_url="base:home")
def takeTeacherAttendance(request, school_branch_id: str):
    teachers = None
    teacher_qs = TeacherProfile.objects.select_related(
                                                "teacher_subject", "school_branch",
                                                "school_branch__manager"
                                            ).all()
    school_branch = SchoolBranch.objects.filter(id=school_branch_id).select_related("manager").first()
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
        return redirect('techsupport:teacherAttendance')
    return redirect('techsupport:teacherAttendance')


@login_required(login_url="base:home")
def viewStudents(request):
    students_to_display = None
    search_input = request.GET.get("q", " ").strip().lower()
    filter_input = request.GET.get("filter")
    class_input = request.GET.get("classId")
    redirect_link = "techsupport:viewStudents"

    school_branches = SchoolBranch.objects.only("name").all()
    branch_names = [branch.name for branch in school_branches]
    logger.debug(f"Branches: {branch_names}")

    students = customFuncs.getStudentProfiles(StudentProfileModel=StudentProfile, session=CURRENT_SESSION)

    if class_input:
        selected_class = Class.objects.get(id=class_input)
        students = students.filter(classes=selected_class)

    student_male_count = students.filter(gender="Male").count()
    student_female_count = students.filter(gender="Female").count()


    if search_input == "deleted" or search_input == "delete":
        # students_to_display = students.filter(user__is_deleted__icontains=1)
        students_to_display = customFuncs.getStudentProfiles(
                                                            StudentProfileModel=StudentProfile, 
                                                            session=CURRENT_SESSION,
                                                            delete_status=1    
                                                        )
    elif search_input == "suspended" or search_input == "suspend":
        students_to_display = students.filter(user__is_suspended__icontains=1)
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
        "student_female_count": student_female_count, "school_branches": branch_names,
    }
    if request.htmx:
        return render(request, "techsupport/components/viewStudentsTable.html", context=context)
    return render(request, "techsupport/pages/viewStudents.html", context=context)


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
            user_.username = username
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
            profile.reistration_number = registration_number
            profile.crgeated_by = request.user
            profile.parent = student_parent
            profile.save()

            logger.info(f"'{student.getFullName}' profile has been updated.".capitalize())
            messages.success(request, f"'{student.getFullName}' profile has been updated.".capitalize())
            return redirect("techsupport:viewStudents")
    else:
        update_user_form = UpdateUserForm(instance=student)
        update_student_profile_form = UpdateStudentProfileForm(instance=student_profile)

    context = {
        "student_profile": student_profile, "student": student, "update_user_form": update_user_form,
        "update_student_profile_form": update_student_profile_form, "student_parent": student_parent
    }
    return render(request, "techsupport/pages/editStudent.html", context=context)


@login_required(login_url="base:home")
def viewParents(request):
    parents_to_display = None
    search_input = request.GET.get("q", " ").strip()
    filter_input = request.GET.get("filter")
    redirect_link = "techsupport:viewParents"

    parents = customFuncs.getParentProfiles(ParentProfile, session=CURRENT_SESSION)

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
    return render(request, "techsupport/pages/viewParents.html", context=context)


@login_required(login_url="base:home")
def viewParent(request, parentId):
    parent = CustomUser.objects.get(id=parentId)
    parent_profile = parent.parentprofile
    children = parent_profile.children.all()

    context = {"parent": parent, "parent_profile": parent_profile, "children": children}
    return render(request, "./techsupport/pages/viewParent.html", context=context)


@login_required(login_url="base:home")
def viewTeachers(request):
    teachers_to_display = None
    search_input = request.GET.get("q", " ").strip()
    filter_input = request.GET.get("filter")
    class_input = request.GET.get("classId")
    redirect_link = "techsupport:viewTeachers"

    school_branches = SchoolBranch.objects.only("name").all()
    branch_names = [branch.name for branch in school_branches]

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
        "teacher_female_count": teacher_female_count, "school_branches": branch_names,
    }
    if request.htmx:
        return render(request, "techsupport/components/viewTeachersTable.html", context=context)
    return render(request, "techsupport/pages/viewTeachers.html", context=context)


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
    male_count = class_participants.filter(gender="Male").count()
    female_count = class_participants.filter(gender="Female").count()

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
            "male_count": male_count, "female_count": female_count
        }
    return render(request, "techsupport/pages/viewTeacherAttendance.html", context=context)


@login_required(login_url="base:home")
def editTeacher(request, teacherId):
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
            return redirect("techsupport:viewTeachers")
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
    return render(request, "techsupport/pages/editTeacher.html", context=context)


@login_required(login_url="base:home")
def viewPrevillagedUsers(request):
    users_to_display = None
    search_input = request.GET.get("q", " ").strip()
    filter_input = request.GET.get("filter")
    class_input = request.GET.get("classId")
    redirect_link = "techsupport:viewPrevillagedUsers"

    school_branches = SchoolBranch.objects.only("name").all()
    branch_names = [branch.name for branch in school_branches]

    previllaged_users = customFuncs.getPrevillagedUsersProfiles(PrevillagedUsersProfileModel=PrevillagedUserProfile)

    previllaged_user_male_count = previllaged_users.filter(gender="Male").count()
    previllaged_user_female_count = previllaged_users.filter(gender="Female").count()

    if search_input == "Suspended" or search_input == "suspended":
        users_to_display = previllaged_users.filter(user__is_suspended__icontains=1)
    elif search_input == "deleted" or search_input == "delete":
        users_to_display = customFuncs.getPrevillagedUsersProfiles(
                            PrevillagedUsersProfileModel=PrevillagedUserProfile, delete_status=1
                        ).filter(user__is_deleted__icontains=1)
    elif search_input:
        users_to_display = previllaged_users.filter(
            Q(user__username__icontains=search_input) | Q(user__email__icontains=search_input) |
            Q(school_branch__name__icontains=search_input) | Q(user__role__icontains=search_input) |
            Q(user__first_name__icontains=search_input) | Q(user__last_name__icontains=search_input) |
            Q(user__last_name__icontains=search_input) | Q(phone_number__icontains=search_input)
        )
    elif filter_input:
        users_to_display = previllaged_users[:int(filter_input)]
    else:
        users_to_display = previllaged_users

    paginator = Paginator(users_to_display, int(customVars.NUMBER_OF_TABLE_ROW)) # Paginate the user queryset
    page_number = request.GET.get("page")
    previllaged_users_page =paginator.get_page(page_number)

    if request.method == "POST":
        form = ManagementActionForm(request.POST, list_of_actions=customVars.MANAGEMENT_ACTIONS)
        if form.is_valid():
            action = form.cleaned_data.get("action")
            selected_previllaged_users = request.POST.getlist('selected_previllaged_users')  # Get selected user IDs
            if not selected_previllaged_users:
                messages.info(request, "Select one or more users to perform an action.")
                return redirect(redirect_link)
            logger.debug(f"Action: {action}")
            logger.debug(f"Selected Previllaged Users IDs: {selected_previllaged_users}")

            customFuncs.objectModificationLog(request, logger, "user(s)")
            if action == "Delete":
                # CustomUser.objects.filter(id__in=selected_previllaged_users).delete()
                CustomUser.objects.filter(id__in=selected_previllaged_users).update(is_deleted=True)
                logger.info("Selected user have been deleted.")
                messages.success(request, "Selected user have been deleted.")
                return redirect(redirect_link)
            elif action == "Undelete":
                CustomUser.objects.filter(id__in=selected_previllaged_users).update(is_deleted=False)
                logger.info("Selected user have been undeleted.")
                messages.success(request, "Selected user have been undeleted.")
                return redirect(redirect_link)
            elif action == "Suspend":
                CustomUser.objects.filter(id__in=selected_previllaged_users).update(is_suspended=True)
                logger.info("Selected user have been suspended.")
                messages.success(request, "Selected user have been suspended.")
                return redirect(redirect_link)
            elif action == "Unsuspend":
                CustomUser.objects.filter(id__in=selected_previllaged_users).update(is_suspended=False)
                logger.info("Selected user have been unsuspended.")
                messages.success(request, "Selected user have been unsuspended.")
                return redirect(redirect_link)
            elif action == "Reset-Password":
                for user_id in selected_previllaged_users:
                    previllaged_user = CustomUser.objects.get(id=user_id)
                    previllaged_user.user.set_password(customVars.DEFAULT_PASSWORD)
                    previllaged_user.user.save()
                logger.info("Passwords have been reset for the selected user.")
                messages.success(request, "Passwords have been reset for the selected user.")
                return redirect(redirect_link)
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = ManagementActionForm(list_of_actions=customVars.MANAGEMENT_ACTIONS)

    context = {
        "previllaged_users": previllaged_users_page, 
        "form": form, "previllaged_users_count": previllaged_users.count(),
        "previllaged_user_male_count": previllaged_user_male_count, 
        "previllaged_user_female_count": previllaged_user_female_count,
        "branch_names": branch_names
    }

    if request.htmx:
        return render(request, "techsupport/components/viewPrevillagedUsersTable.html", context=context)

    return render(request, "techsupport/pages/viewPrevillagedUsers.html", context=context)


@login_required(login_url="base:home")
def viewPrevillagedUser(request, userId):
    previllaged_user = CustomUser.objects.get(id=userId)
    previllaged_user_profile = PrevillagedUserProfile.objects.get(user=previllaged_user)

    context = {"previllaged_user": previllaged_user, "previllaged_user_profile": previllaged_user_profile}
    return render(request, "techsupport/pages/viewPrevillagedUser.html", context=context)


@login_required(login_url="base:home")
def editPrevillagedUser(request, userId):
    previllaged_user = CustomUser.objects.get(id=userId)
    previllaged_user_profile = PrevillagedUserProfile.objects.get(user=previllaged_user)

    if request.method == "POST":
        update_user_form = UpdateUserForm(request.POST, instance=previllaged_user)
        update_previllaged_user_profile_form = PrevillagedUserProfileForm(request.POST, instance=previllaged_user_profile)
        customFuncs.objectModificationLog(request, logger, "student account & profile")
        if update_user_form.is_valid() and update_previllaged_user_profile_form.is_valid():
            username = update_user_form.cleaned_data.get("username")
            if username == "":
                username = customFuncs.generateUserEmail(
                                first_name=previllaged_user.first_name,
                                last_name=previllaged_user.last_name,
                                middle_name=previllaged_user.middle_name
                            )
            email = update_user_form.cleaned_data.get("email")
            if email == "":
                email = customFuncs.generateUserEmail(
                                first_name=previllaged_user.first_name, 
                                last_name=previllaged_user.last_name, 
                                middle_name=previllaged_user.middle_name
                            )
            user_ = update_user_form.save(commit=False)
            user_.username = username
            user_.email = email
            user_.save()

            profile = update_previllaged_user_profile_form.save(commit=False)
            profile.created_by = request.user
            profile.save()

            logger.info(f"'{user_.getFullName}' profile has been updated.".capitalize())
            messages.success(request, f"'{user_.getFullName}' profile has been updated.".capitalize())
            return redirect("techsupport:viewPrevillagedUsers")
        else:
            customFuncs.displayFormErrors(request, update_user_form, messages, logger)
            customFuncs.displayFormErrors(request, update_previllaged_user_profile_form, messages, logger)
    else:
        update_user_form = UpdateUserForm(instance=previllaged_user)
        update_previllaged_user_profile_form = PrevillagedUserProfileForm(instance=previllaged_user_profile)

    context = {
        "update_user_form": update_user_form, "update_previllaged_user_profile_form": update_previllaged_user_profile_form,
        "previllaged_user": previllaged_user, "previllaged_user_profile": previllaged_user_profile,           
    }
    return render(request, "techsupport/pages/editPrevillagedUser.html", context=context)


@login_required(login_url="base:home")
def createSession(request):
    sessions_to_display = None
    sessions = Session.objects.all()
    filter_input = request.GET.get("filter")

    if filter_input == "all":
        sessions_to_display = sessions
    if filter_input:
        sessions_to_display = sessions[:int(filter_input)]
    else:
        sessions_to_display = sessions[:100]

    if request.method == "POST":
        form = CreateSessionForm(request.POST)
        if form.is_valid():
            session_obj = form.save(commit=False)
            session_obj.created_by = request.user
            session_obj.save()

            logger.info(f"Session created successfully.")
            messages.success(request, f"Session created successfully.")
            return redirect("techsupport:createSession")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateSessionForm()
    
    context = {"sessions_to_display": sessions_to_display, "form": form, "page_title": "Create Session"}
    return render(request, "techsupport/pages/createSession.html", context=context)


@login_required(login_url="base:home")
def editSession(request, sessionId):
    sessions = Session.objects.all()
    session = Session.objects.get(id=sessionId)

    filter_input = request.GET.get("filter")

    if filter_input == "all":
        sessions_to_display = sessions
    if filter_input:
        sessions_to_display = sessions[:int(filter_input)]
    else:
        sessions_to_display = sessions[:100]

    if request.method == "POST":
        form = CreateSessionForm(request.POST, instance=session)
        if form.is_valid():
            session_obj = form.save(commit=False)
            session_obj.created_by = request.user
            session_obj.save()
            logger.info(f"Session updated successfully.")
            messages.success(request, f"Session updated successfully.")
            return redirect("techsupport:createSession")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateSessionForm(instance=session)

    form = CreateSessionForm(instance=session)

    context = {"sessions_to_display": sessions_to_display, "session": session, "form": form, "page_title": "Update Session"}
    return render(request, "techsupport/pages/createSession.html", context=context)


@login_required(login_url="base:home")
def createSubject(request):
    subjects = Subject.objects.prefetch_related("teachers", "topics").all().order_by("-created_on")

    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "subject")
        form = CreateSubjectForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get("name")
            if Subject.objects.filter(name=subject).exists():
                messages.success(request, f"Subject Already Exists.")
                return redirect("techsupport:createSubject")   
            else:
                subject_obj = form.save(commit=False)
                subject_obj.created_by = request.user
                subject_obj.save()

                logger.info(f"Subject '{subject}' Added.")
                messages.success(request, f"Subject '{subject}' Added.")   
                return redirect("techsupport:createSubject")   
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateSubjectForm()

    context = {"subjects": subjects, "form": form, "page_title": "Create Subject"}
    return render(request, "techsupport/pages/createSubject.html", context=context)


@login_required(login_url="base:home")
def editSubject(request, subjectId):
    subjects = Subject.objects.prefetch_related("teachers", "topics").all().order_by("-created_on")
    subject = Subject.objects.get(id=subjectId)

    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "subject")
        form = CreateSubjectForm(request.POST, instance=subject)
        if form.is_valid():
            subject_obj = form.save(commit=False)
            subject_obj.created_by = request.user
            subject_obj.save()
            
            logger.info(f"Subject '{subject}' has been updated.")
            messages.success(request, f"Subject '{subject}' has been updated.")
            return redirect("techsupport:createSubject")   
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateSubjectForm(instance=subject)

    context = {"subjects": subjects, "form": form, "page_title": "Update Subject"}
    return render(request, "techsupport/pages/createSubject.html", context=context)


@login_required(login_url="base:home")
def createTopic(request):
    topics_to_display = None
    topics = Topic.objects.select_related("subject" ).all().order_by("-created_on")

    filter_input = request.GET.get("filter")

    if filter_input == "all":
        topics_to_display = topics
    elif filter_input:
        topics_to_display = topics[:int(filter_input)]
    else:
        topics_to_display = topics[:50]

    if request.method == "POST":
        form = CreateTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.created_by = request.user
            topic.save()
            logger.info(f"Subject '{topic.name}' Added.")
            messages.success(request, f"Subject '{topic.name}' Added.")   
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)

    
    form = CreateTopicForm()

    context = {"form": form, "topics": topics_to_display}

    if request.htmx:
        return render(request, "techsupport/components/topicsTable.html", context=context)
    
    return render(request, "techsupport/pages/createTopic.html", context=context)


@login_required(login_url="base:home")
def editTopic(request, topicId):
    topic = Topic.objects.get(id=topicId)

    if request.method == "POST":
        form = CreateTopicForm(request.POST, instance=topic)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.created_by = request.user
            topic.save()
            logger.info(f"Subject '{topic.name}' has been updated.")
            messages.success(request, f"Subject '{topic.name}' has been updated.")   
            return redirect("techsupport:createTopic")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateTopicForm(instance=topic)

    context = {"form": form}
    return render(request, "techsupport/pages/editTopic.html", context=context)


@login_required(login_url="base:home")
def createSchoolBranch(request):
    school_branches = SchoolBranch.objects.select_related("manager").all().order_by("-created_on")

    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "school branch")
        form = CreateSchoolBranchForm(request.POST)
        if form.is_valid():
            school_branch_obj = form.save(commit=False)
            school_branch_obj.created_by = request.user
            school_branch_obj.save()

            logger.info(f"Branch has been Created Successfully.")
            messages.success(request, f"Branch has been Created Successfully.")
            return redirect("techsupport:createSchoolBranch")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateSchoolBranchForm()

    context = {"form": form, "school_branches": school_branches, "page_title": "Create Cluster"}
    return render(request, "techsupport/pages/createSchoolBranch.html", context=context)


@login_required(login_url="base:home")
def editSchoolBranch(request, schoolBranchId):
    school_branches = SchoolBranch.objects.select_related("manager").all().order_by("-created_on")
    school_branch = SchoolBranch.objects.filter(id=schoolBranchId).first()

    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "school branch")
        form = CreateSchoolBranchForm(request.POST, instance=school_branch)
        if form.is_valid():
            school_branch_obj = form.save(commit=False)
            school_branch_obj.created_by = request.user
            school_branch_obj.save()

            logger.info(f"School Branch Updated Successfully.")
            messages.success(request, f"School Branch Updated Successfully.")
            return redirect("techsupport:createSchoolBranch")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateSchoolBranchForm(instance=school_branch)

    context = {
            "school_branches": school_branches, "school_branch": school_branch, 
            "form": form, "page_title": "Update Cluster"
        }
    return render(request, "techsupport/pages/createSchoolBranch.html", context=context)


@login_required(login_url="base:home")
def createClass(request):
    all_class = Class.objects.select_related("section", "name").all().prefetch_related("subjects")

    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "class")
        form = CreateClassForm(request.POST)
        if form.is_valid():
            logger.debug(f"Class Data: {form.cleaned_data}")
            form.save()
            logger.info(f"Class has been Created Successfully.")
            messages.success(request, f"Class has been Created Successfully.")
            return redirect("techsupport:createClass")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateClassForm()
    
    context = {"form": form, "all_class": all_class}
    return render(request, "techsupport/pages/createClass.html", context=context)


@login_required(login_url="base:home")
def editClass(request, classId):
    class_to_edit = Class.objects.filter(id=classId).first()
    class_name_obj = ClassName.objects.filter(name__icontains=class_to_edit.name.name)
    logger.debug(f"class to edit: {class_to_edit}")
    logger.debug(f"class_name_obj: {class_name_obj}")

    if request.method == "POST":
        form = EditClassForm(request.POST, instance=class_to_edit)
        if form.is_valid():
            new_class_name = form.cleaned_data.get("new_class_name")
            # class_name_obj.name = new_class_name 
            class_name_obj.update(name=new_class_name)
            class_to_save = form.save(commit=False)
            class_to_save.name.name = new_class_name
            class_to_save.save()

            logger.info(f"Class Updated Successfully.")
            messages.success(request, f"Class Updated Successfully.")
            return redirect("techsupport:createClass")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = EditClassForm(instance=class_to_edit)

    context = {"class_to_edit": class_to_edit, "form": form}
    return render(request, "techsupport/pages/editClass.html", context=context)


@login_required(login_url="base:home")
def createCourse(request):
    courses = Course.objects.all().order_by("-created_on")

    if request.method == "POST":
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=True)
            course.created_by = request.user
            course.save()
            logger.info(f"Course Created Successfully.")
            messages.success(request, f"Course Created Successfully.")
            return redirect("techsupport:createCourse")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateCourseForm()

    context = {"form": form, "courses": courses}
    return render(request, "techsupport/pages/createCourse.html", context=context)


@login_required(login_url="base:home")
def createQuestion(request):
    question_image = None
    option_image = None
    question = None
    if request.method == "POST":
        form = CreateQuestionForm(request.POST, request.FILES)
        option_formset = OptionFormSet(request.POST, request.FILES, instance=question)
        logger.debug(f"Create question Form: {request.POST}")
        if form.is_valid() and option_formset.is_valid():
            question = form.save(commit=False)
            logger.debug(f"Create question Form Cleaned DAta: {form.cleaned_data}")
            
            image = form.cleaned_data.get("image")
            if image:
                try:
                    question_image = customFuncs.resizeImage(image, width=600, height=600)
                    question.image = question_image
                except:
                    messages.error(request, f"Wrong image format. Only jpeg/jpg format is allowed.")
                    return redirect("techsupport:createQuestion")
            else:
                pass
            question.created_by = request.user
            question.save()

            options = option_formset.save(commit=False)
            for option in options:
                option.created_by = request.user
                option.question = question 
                option.save()
            logger.info(f"'{question.subject.name}' question added.".capitalize())
            messages.success(request, f"'{question.subject.name}' question added.".capitalize())
            return redirect("techsupport:createQuestion")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
            customFuncs.displayFormErrors(request, option_formset, messages, logger)
    else:
        form = CreateQuestionForm()
        option_formset = OptionFormSet()

    context = {"form": form, "option_formset": option_formset}
    return render(request, "techsupport/pages/createQuestion.html", context=context)


login_required(login_url="base:home")
def editQuestion(request, questionId):
    question_image = None
    page = request.GET.get("page")
    question = get_object_or_404(Question, id=questionId)

    if request.method == "POST":
        form = EditQuestionForm(request.POST, request.FILES, instance=question, subject_name=question.subject.name)
        if form.is_valid():
            logger.debug(f"CLEANED DATA: {form.cleaned_data}")
            image = form.cleaned_data.get("image")
            question = form.save(commit=False)
            if image:
                try:
                    question_image = customFuncs.resizeImage(image, width=600, height=600)
                    question.image = question_image
                except:
                    messages.error(request, f"Wrong image format. Only jpeg/jpg format is allowed.")
                    return redirect("techsupport:editQuestion", questionId=question.id)
            else:
                pass
            question.created_by = request.user
            question.save()
            
            messages.success(request, f"'{question.subject.name}' question updated successfully.")
            if page == "viewquestionspage":
                return redirect("techsupport:viewQuestions")
            elif page == "previewcbtexamination":
                return redirect("techsupport:previewCBTExamination", cbtCategoryId=question.cbt.cbt_category.id)
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = EditQuestionForm(instance=question, subject_name=question.subject.name)

    context = {"form": form, "question": question,}
    return render(request, "techsupport/pages/editQuestion.html", context=context)


@login_required(login_url="base:home")
def editQuestionOptions(request, questionId):
    page = request.GET.get("page")
    question = get_object_or_404(Question, id=questionId)
    
    # Define formset without explicitly including 'id' field
    OptionFormSet = modelformset_factory(
        Option,
        fields=('content', 'is_correct', 'image'),  # Removed 'id' field
        extra=0,
        can_delete=True
    )
    
    if request.method == "POST":
        option_formset = OptionFormSet(request.POST, request.FILES, queryset=question.options.all())
        
        if option_formset.is_valid():
            for option_form in option_formset:
                if option_form.cleaned_data.get('DELETE'):
                    if option_form.instance.id:
                        option_form.instance.delete()
                else:
                    option = option_form.save(commit=False)
                    option.question = question
                    option.created_by = request.user
                    option.save()
            messages.success(request, "Options updated successfully.")
            if page == "viewquestionspage":
                return redirect("techsupport:viewQuestions")
            elif page == "previewcbtexamination":
                return redirect("techsupport:previewCBTExamination", cbtCategoryId=question.cbt.cbt_category.id)
        else:
            logger.debug("Option formset errors: %s", option_formset.errors)
            messages.error(request, "Please correct the errors in the form.")
    else:
        option_formset = OptionFormSet(queryset=question.options.all())

    context = {
        "question": question,
        "option_formset": option_formset,
    }
    return render(request, "techsupport/pages/editQuestionOptions.html", context=context)


def topicsOptions(request):
    subject_id = request.GET.get("subject")
    subject = Subject.objects.get(id=subject_id)
    topics = subject.topics.all()
    logger.debug(f"Topics: {topics}")
    
    context = {"topics": topics}
    return render(request, "techsupport/components/topicsOptions.html", context=context)


@login_required(login_url="base:home")
def viewQuestions(request):
    questions = Question.objects.select_related(
                        "subject", "topic", "created_by"
                    ).prefetch_related(
                        "cbt", "exam_practice", "exam",
                    ).all()
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

    
    if filter_input:
        paginator = Paginator(questions, int(filter_input))
    else:
        paginator = Paginator(questions, int(customVars.NUMBER_OF_TABLE_ROW))
    page_number = request.GET.get("page")
    questions_page =paginator.get_page(page_number)
    
    context = {"questions_to_display": questions_page, "questions": questions, "subjects": subjects}

    if request.htmx:
        return render(request, "techsupport/components/viewQuestionsTable.html", context=context)

    return render(request, "techsupport/pages/viewQuestions.html", context=context)


@login_required(login_url="base:home")
def viewQuestionWIthOptions(request, questionId):
    question = Question.objects.get(id=questionId)

    context = {"question": question, "option_labels": customVars.OPTION_LABELS}
    return render(request, "techsupport/pages/viewQuestionWIthOptions.html", context=context)






