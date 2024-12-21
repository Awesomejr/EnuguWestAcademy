import logging
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.forms import modelformset_factory


from base.models import (CustomUser, StudentProfile, ParentProfile, SchoolBranch, Subject, 
                        TeacherProfile, Session, Class, Topic
                        )
from base.forms import (StudentAttendanceSearchForm, CreateTopicForm)
from techSupport.forms import CreateQuestionForm, EditQuestionForm, OptionFormSet, CreateOptionForm
from attendance.models import StudentAttendance, TeacherAttendance
from examination.models import Exam, Question, Option, CBTCategory

from utilities import customFuncs, customVars

CURRENT_SESSION = customFuncs.getCurrentSession(Session)
logger = logging.getLogger(__name__)


# Create your views here.
@login_required(login_url="base:home")
def dashboard(request):
    teacher = request.user
    teacher_profile = teacher.teacherprofile

    number_to_display = 10
    school_branches = SchoolBranch.objects.select_related("manager").all()
    subjects = Subject.objects.all()
    students = customFuncs.getStudentProfiles(
                                            StudentProfileModel=StudentProfile, 
                                            session=CURRENT_SESSION,
                                        ).filter(
                                            school_branch=teacher_profile.school_branch
                                        )
    parents = customFuncs.getParentProfiles(ParentProfileModel=ParentProfile, session=CURRENT_SESSION)
    teachers = customFuncs.getTeacherProfiles(TeacherProfileModel=TeacherProfile).filter(
                                                school_branch=teacher_profile.school_branch
                                            )
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

    context = {"total_school_branches": school_branches.count(), "total_subjects": subjects.count(),
                "students_preview": students[:number_to_display], "parents_preview": parents[:number_to_display],
                "students": students, "parents": parents,
                "students_in_each_branch": students_in_each_branch,
                "teachers_in_each_branch": teachers_in_each_branch,
                "branch_name": branch_name, "number_of_students": number_of_students,
                "teachers": teachers, "exams": exams, "teacher_branch_name": teacher_branch_name,
                "number_of_teachers": number_of_teachers,
            }
    return render(request, "./teacher/pages/dashboard.html", context=context)


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
    
    return render(request, "teacher/pages/createTopic.html", context=context)


@login_required(login_url="base:home")
def viewClass(request):
    teacher = request.user
    teacher_profile = teacher.teacherprofile
    teacher_class = teacher_profile.assigned_class.all()
    initial_class = teacher_class.first()
    students = StudentProfile.objects.select_related(
                                            "user", "classes__name", "session",
                                            "school_branch__manager", "course"
                                        ).filter(
                                            classes=initial_class, 
                                            session=CURRENT_SESSION,
                                            school_branch=teacher_profile.school_branch,
                                        )
    male_count = students.filter(gender="Male").count()
    female_count = students.filter(gender="Female").count()

    context = {
        "teacher_class": teacher_class, "teacher_profile": teacher_profile, 
        "teacher": teacher, "class_participants": students, "student_class": initial_class,
        "male_count": male_count, "female_count": female_count,
    }
    return render(request, "teacher/pages/viewClass.html", context=context)


@login_required(login_url="base:home")
def loadClassStudents(request, classId):
    teacher = request.user
    teacher_profile = teacher.teacherprofile

    student_class = Class.objects.select_related("name", "section").filter(id=classId).first()
    students = StudentProfile.objects.select_related(
                                            "user", "classes__name", "session",
                                            "school_branch__manager", "course"
                                        ).filter(
                                            classes=student_class, 
                                            session=CURRENT_SESSION,
                                            school_branch=teacher_profile.school_branch,
                                        )
    male_count = students.filter(gender="Male").count()
    female_count = students.filter(gender="Female").count()

    context = {
        "class_participants": students, "male_count": male_count, 
        "female_count": female_count, "student_class": student_class
    }
    return render(request, "teacher/components/previewClassStudents.html", context=context)


@login_required(login_url="base:home")
def viewAttendance(request):
    teacher = request.user
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
    
    return render(request, "teacher/pages/viewAttendance.html", context=context)


@login_required(login_url="base:home")
def createQuestion(request):
    question = None
    if request.method == "POST":
        form = CreateQuestionForm(request.POST, request.FILES)
        option_formset = OptionFormSet(request.POST, request.FILES, instance=question)
        logger.debug(f"Create question Form: {request.POST}")
        if form.is_valid() and option_formset.is_valid():
            logger.debug(f"Create question Form Cleaned DAta: {form.cleaned_data}")
            question = form.save(commit=False)
            question.created_by = request.user
            question.save()

            options = option_formset.save(commit=False)
            for option in options:
                option.created_by = request.user
                option.question = question 
                option.save()
            logger.info(f"'{question.subject.name}' question added.".capitalize())
            messages.success(request, f"'{question.subject.name}' question added.".capitalize())
            return redirect("teacher:createQuestion")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
            customFuncs.displayFormErrors(request, option_formset, messages, logger)
    else:
        form = CreateQuestionForm()
        option_formset = OptionFormSet()

    context = {"form": form, "option_formset": option_formset}
    return render(request, "teacher/pages/createQuestion.html", context=context)


login_required(login_url="base:home")
def editQuestion(request, questionId):
    question = get_object_or_404(Question, id=questionId)

    if request.method == "POST":
        form = EditQuestionForm(request.POST, request.FILES, instance=question, subject_name=question.subject.name)
        if form.is_valid():
            logger.debug(f"CLEANED DATA: {form.cleaned_data}")
            form.save()
            messages.success(request, f"'{question.subject.name}' question updated successfully.")
            return redirect("teacher:viewQuestions")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = EditQuestionForm(instance=question, subject_name=question.subject.name)

    context = {"form": form, "question": question,}
    return render(request, "teacher/pages/editQuestion.html", context=context)


@login_required(login_url="base:home")
def editQuestionOptions(request, questionId):
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
            return redirect("teacher:viewQuestions")
        else:
            logger.debug("Option formset errors: %s", option_formset.errors)
            messages.error(request, "Please correct the errors in the form.")
    else:
        option_formset = OptionFormSet(queryset=question.options.all())

    context = {
        "question": question,
        "option_formset": option_formset,
    }
    return render(request, "teacher/pages/editQuestionOptions.html", context=context)


def topicsOptions(request):
    subject_id = request.GET.get("subject")
    subject = Subject.objects.get(id=subject_id)
    topics = subject.topics.all()
    logger.debug(f"Topics: {topics}")
    
    context = {"topics": topics}
    return render(request, "techsupport/components/topicsOptions.html", context=context)


@login_required(login_url="base:home")
def viewQuestions(request):
    questions = Question.objects.select_related("exam", "cbt", "exam_practice", 
                                                "subject", "topic", "created_by")
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

    return render(request, "teacher/pages/viewQuestions.html", context=context)


@login_required(login_url="base:home")
def viewQuestionWIthOptions(request, questionId):
    question = Question.objects.get(id=questionId)

    context = {"question": question, "option_labels": customVars.OPTION_LABELS}
    return render(request, "teacher/pages/viewQuestionWIthOptions.html", context=context)

