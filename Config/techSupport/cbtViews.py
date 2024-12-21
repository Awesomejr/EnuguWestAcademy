import logging
import pprint
import datetime
import json
import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Avg, Case, When, IntegerField, Prefetch
from django.core.paginator import Paginator
from django.db.models.functions import Coalesce

from utilities.testData import testData

from .forms import (CreateCBTExamForm,
                    CreateCBTCategoryForm, CreateCBTQuestionsForm
                    )
from base.models import (ParentProfile, StudentProfile, CustomUser, TeacherProfile, 
                        Session, SchoolBranch, Subject, Topic, Class, ClassSection,
                        Course
                        )
from base.forms import StudentAttendanceSearchForm, ManagementActionForm
from examination.models import (Question, CBTExam, CBTCategory, CBTResult, StudentCBTAnswer, Option
                                )

from utilities import customFuncs, customVars

logger = logging.getLogger(__name__)
CURRENT_SESSION = customFuncs.getCurrentSession(Session)


@login_required(login_url="base:home")
def createCBTCategory(request):
    if request.method == "POST":
        form = CreateCBTCategoryForm(request.POST)
        if form.is_valid():
            cbt_category = form.save(commit=False)
            cbt_category.created_by=request.user
            cbt_category.save()
            logger.debug(f"CBT Category Created.")
            messages.success(request, f"CBT Category Created.")
            return redirect("techsupport:createCBTExam")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateCBTCategoryForm()

    context = {"form": form, "page_title": "Create"}
    return render(request, "techsupport/pages/createCBTCategory.html", context=context)


@login_required(login_url="base:home")
def editCBTCategory(request, cbtCategoryId):
    cbt_category = CBTCategory.objects.select_related(
            "session", "assigned_class", "supervisor"
            ).prefetch_related("school_branch").get(id=cbtCategoryId)
    logger.debug(f"Cat. CBT {cbt_category}")
    if request.method == "POST":
        form = CreateCBTCategoryForm(request.POST, instance=cbt_category)
        if form.is_valid():
            form.save()
            logger.debug(f"CBT Category Update.")
            messages.success(request, f"CBT Category Update.")
            return redirect("techsupport:previewCBTCategory")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateCBTCategoryForm(instance=cbt_category)

    context = {"form": form, "page_title": "Update"}
    return render(request, "techsupport/pages/createCBTCategory.html", context=context)



@login_required(login_url="base:home")
def createCBTExam(request):
    if request.method == "POST":
        form = CreateCBTExamForm(request.POST)
        if form.is_valid():
            subjects = form.cleaned_data.get("subjects")

            if not (3 <= len(subjects) <= 4):
                messages.info(request, "Selected Subjects must be either 3 or 4.")
                return redirect("techsupport:createCBTExam")

            session = form.cleaned_data.get("session")
            cbt_category = form.cleaned_data.get("cbt_category")
            # supervisor = form.cleaned_data.get("supervisor")

            if cbt_category.exams.all():
                messages.info(request, "This CBT already has existing exams.")
                return redirect("techsupport:createCBTExam")

            try:
                for subject in subjects:
                    subject_obj = Subject.objects.get(name__icontains=subject)
                    CBTExam.objects.create(
                        cbt_category=cbt_category,
                        session=session,
                        subject=subject_obj,
                        created_by=request.user,
                    )
                logger.info(f"Created {len(subjects)} exams under '{cbt_category}'.")
                messages.success(request, f"{cbt_category} created with {len(subjects)} subjects.")
            except Subject.DoesNotExist:
                messages.error(request, f"Subject {subject} does not exist.")
                logger.exception(f"Subject {subject} not found.")
            return redirect("techsupport:createCBTQuestion", cbtCategoryId=cbt_category.id)
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateCBTExamForm()

    context = {"form": form}
    return render(request, "techsupport/pages/createCBTExam.html", context=context)


@login_required(login_url="base:home")
def createCBTQuestion(request, cbtCategoryId):
    questions_to_display = None
    topics = None
    
    cbt_category = CBTCategory.objects.get(id=cbtCategoryId)
    cbt_exams = cbt_category.exams.select_related("subject").all()

    # Dynamic filtering for topics based on exams' subjects
    subject_names = [exam.subject.name for exam in cbt_exams]
    toipcs = Topic.objects.filter(subject__name__in=subject_names).select_related("subject", "created_by")

    # Process filtering
    filter_input = request.GET.get("filter")
    subject = request.GET.get("subject")
    topic = request.GET.get("topic")

    # Filter questions based on user input
    questions = Question.objects.defer("exam", "cbt", "exam_practice").select_related(
                                                "topic", "subject", "created_by"
                                            ).prefetch_related("cbt").filter(subject__name__in=subject_names)
    if subject and topic:
        questions = questions.filter(
            subject__name__icontains=subject,
            topic__name__icontains=topic
        )
    elif subject:
        questions = questions.filter(
            subject__name__icontains=subject
        )
    elif filter_input == "all":
        questions = questions
    elif filter_input and filter_input.isdigit():
        questions = questions[:int(filter_input)]
    else:
        questions = questions

    if filter_input and filter_input.isdigit():
        paginator = Paginator(questions, int(filter_input)) # Paginate the students queryset
    else:
        paginator = Paginator(questions, int(customVars.NUMBER_OF_TABLE_ROW)) # Paginate the students queryset
    page_number = request.GET.get("page")
    questions_page =paginator.get_page(page_number)

    # Handle POST request for question selection
    if request.method == "POST" and subject:
        selected_question_ids = request.POST.getlist("selected_questions")  # Retrieve selected questions
        cbt_exam = CBTExam.objects.prefetch_related("cbt_questions").get(cbt_category=cbt_category, subject__name__icontains=subject)

        if not cbt_exam:
            messages.error(request, "Selected subject not found in CBT exams.")
        else:
            cbt_questions = cbt_exam.cbt_questions.all()
            questions_to_update = questions.filter(id__in=selected_question_ids)
            # questions_to_update.update(cbt=cbt_exam)

            for question in questions_to_update:
                if question in cbt_questions:
                    pass
                else:
                    question.cbt.add(cbt_exam)
            messages.success(request, f"Selected questions added to '{cbt_exam.getExamName}'")
            return redirect("techsupport:createCBTQuestion", cbtCategoryId=cbtCategoryId)

    # form = CreateCBTQuestionsForm()
    context = {
        # "form": form,
        "cbt_category": cbt_category,
        "cbt_exams": cbt_exams,
        "questions": questions_page,
        "subject": subject,
        "topics": topics,
        "subject_names": subject_names
    }

    if request.htmx:
        return render(request, "techsupport/components/cbtQuestionsTable.html", context=context)

    return render(request, "techsupport/pages/createCBTQuestion.html", context=context)


@login_required(login_url="base:home")
def removeCBTQuestion(request, cbtCategoryId, cbtExamId, questionId):
    cbt_category = CBTCategory.objects.get(id=cbtCategoryId)
    cbt_exam = CBTExam.objects.get(id=cbtExamId, cbt_category=cbt_category)
    question = Question.objects.defer("exam", "exam_practice").select_related(
                                                "topic", "subject", "created_by"
                                            ).filter(id=questionId).first()
    question.cbt.remove(cbt_exam)
    messages.success(request, f"Question has been removed fron this CBT Examination.")
    return redirect("techsupport:previewCBTExamination", cbtCategoryId=cbtCategoryId)


@login_required(login_url="base:home")
def cbtExamsOptions(request):
    cbt_category_id = request.GET.get("cbt_category")
    logger.debug(f"CBT Category ID; {cbt_category_id}")
    cbt_category = CBTCategory.objects.get(id=cbt_category_id)
    cbt_exams = cbt_category.exams.all()

    context = {"cbt_exams": cbt_exams}
    return render(request, "techsupport/components/cbtExamsOptions.html", context=context)


@login_required(login_url="base:home")
def previewCBTCategory(request):
    cbt_categories = CBTCategory.objects.select_related(
        "assigned_class", "assigned_class__name", "assigned_class__section", 
        "session", "created_by", "supervisor"
    ).prefetch_related("exams__subject").all()

    context = {"cbt_categories": cbt_categories}
    return render(request, "techsupport/pages/previewCBTCategory.html", context=context)


@login_required(login_url="base:home")
def publishCBTCategory(request, cbtCategoryId):
    cbt_category = CBTCategory.objects.get(id=cbtCategoryId)

    if cbt_category.published:
        cbt_category.published=False
        cbt_category.save()
        messages.success(request, f"CBT has been unpublished.".capitalize())
    else:
        cbt_category.published=True
        cbt_category.save()
        messages.success(request, f"CBT has been published.".capitalize())
    return redirect("techsupport:previewCBTCategory")


@login_required(login_url="base:home")
def previewCBTExamination(request, cbtCategoryId):
    cbt_category = CBTCategory.objects.get(id=cbtCategoryId)
    cbt_exams = cbt_category.exams.all()
    initial_exam =cbt_exams.order_by("?").first()

    context = {"cbt_exams": cbt_exams, "cbt_category": cbt_category, "cbt_exam": initial_exam, "option_labels": customVars.OPTION_LABELS}
    return render(request, "techsupport/pages/previewCBTExamination.html", context=context)


@login_required(login_url="base:home")
def loadCBTExamQuestions(request, cbtExamId):
    cbt_exam = CBTExam.objects.get(id=cbtExamId)
    questions = cbt_exam.cbt_questions.all()

    context = {"questions": questions, "cbt_exam": cbt_exam, "option_labels": customVars.OPTION_LABELS}
    return render(request, "techsupport/components/cbtExamQuestionsSection.html", context=context)


@login_required(login_url="base:home")
def viewCBTScores(request):
    page = request.GET.get("page")
    
    cbt_categories = CBTCategory.objects.select_related(
            "assigned_class__name", "assigned_class__section", "session", "supervisor", "created_by"
            ).prefetch_related("exams__subject").all()


    context = {"cbt_categories": cbt_categories}
    if page == "guest":
        return render(request, "guest/pages/viewCBTScores.html", context=context)
    elif page == "manager":
        return render(request, "manager/pages/viewCBTScores.html", context=context)
    
    return render(request, "techsupport/pages/viewCBTScores.html", context=context)


@login_required(login_url="base:home")
def viewCBTCategoryExams(request, cbtCategoryId):
    cbt_category = CBTCategory.objects.select_related(
            "assigned_class", "session", "supervisor", "created_by"
            ).prefetch_related("exams").filter(id=cbtCategoryId).first()
    exams = cbt_category.exams.all()

    context = {
        'cbt_category': cbt_category,
        'exams': exams,
    }
    return render(request, "techsupport/pages/viewCBTCategoryExams.html", context=context)


# @login_required(login_url="base:home")
# def viewCBTAnalysis(request, cbtCategoryId):
#     cbt_category = CBTCategory.objects.defer(
#         "created_by", "supervisor", "exam_date", "start_time",
#         "end_time", "duration", "published"
#     ).select_related(
#         "assigned_class", "assigned_class__name", "assigned_class__section"
#     ).filter(id=cbtCategoryId).first()

#     exams = CBTExam.objects.defer("assigned_class").select_related(
#         "session",
#         "cbt_category", "subject", "supervisor", "created_by", "teacher"
#     ).prefetch_related("cbt_questions").filter(cbt_category=cbt_category)

#     school_branch = request.GET.get("school_branch")
#     logger.debug(f"School Branch: {school_branch}")

#     # Retrieve all CBTResults for this category at once
#     student_results = CBTResult.objects.select_related(
#         "student", "student__user", "student__school_branch", "student__school_branch__manager",
#         "cbt_category", "cbt_exam", "cbt_exam__subject"
#     ).filter(
#         cbt_category=cbt_category,
#         student__school_branch=school_branch if school_branch else None
#     )

#     students_data = []
#     topic_analysis = {}

#     # Bulk fetching selected options for all students
#     all_selected_answers = {}
#     for result in student_results:
#         all_selected_answers.update(result.answers)

#     selected_option_ids = [
#         student_answer.get('selected')
#         for answers in all_selected_answers.values()
#         for student_answer in answers.values() if student_answer
#     ]
#     selected_options = Option.objects.filter(id__in=selected_option_ids)
#     selected_options_by_id = {option.id: option for option in selected_options}

#     for result in student_results:
#         student_data = {
#             'student': result.student,
#             'total_score': 0,
#             'correct_answers': 0,
#             'incorrect_answers': 0,
#             'exam_scores': []
#         }

#         for exam in exams:
#             questions = Question.objects.defer("exam", "exam_practice").select_related(
#                 "subject", "subject__created_by", "topic", "topic__subject",
#                 "topic__created_by", "topic__subject__created_by", "created_by"
#             ).prefetch_related(
#                 Prefetch(
#                     'options',
#                     queryset=Option.objects.filter(is_correct=True),
#                     to_attr='correct_option_list'
#                 ),
#                 "cbt"
#             ).filter(cbt=exam)

#             student_answers = result.answers.get(str(exam.id), {})

#             exam_correct_answers = 0
#             exam_incorrect_answers = 0

#             for question in questions:
#                 correct_option = question.correct_option_list[0] if question.correct_option_list else None
#                 student_answer = student_answers.get(str(question.id))
#                 selected_option = selected_options_by_id.get(student_answer.get('selected')) if student_answer else None

#                 if correct_option and selected_option and correct_option.id == selected_option.id:
#                     exam_correct_answers += 1
#                     topic = question.topic
#                     if topic:
#                         topic_analysis[topic.name] = topic_analysis.get(topic.name, {'correct': 0, 'incorrect': 0, 'subject': topic.subject.name})
#                         topic_analysis[topic.name]['correct'] += 1
#                 elif selected_option:
#                     exam_incorrect_answers += 1
#                     topic = question.topic
#                     if topic:
#                         topic_analysis[topic.name] = topic_analysis.get(topic.name, {'correct': 0, 'incorrect': 0, 'subject': topic.subject.name})
#                         topic_analysis[topic.name]['incorrect'] += 1

#             exam_score = (exam_correct_answers / questions.count() * 100) if questions.count() > 0 else 0
#             student_data['total_score'] += exam_score
#             student_data['correct_answers'] += exam_correct_answers
#             student_data['incorrect_answers'] += exam_incorrect_answers
#             student_data['exam_scores'].append({
#                 'exam': exam,
#                 'correct_answers': exam_correct_answers,
#                 'incorrect_answers': exam_incorrect_answers,
#                 'score_percentage': exam_score
#             })

#         student_data['total_score'] = student_data['total_score'] / len(exams) if exams else 0
#         students_data.append(student_data)

#     topic_summary = [
#         {
#             'topic': topic,
#             'subject': topic_analysis[topic]['subject'],
#             'correct': topic_analysis[topic]['correct'],
#             'incorrect': topic_analysis[topic]['incorrect'],
#             'total': topic_analysis[topic]['correct'] + topic_analysis[topic]['incorrect'],
#             'percentage': (topic_analysis[topic]['correct'] / (topic_analysis[topic]['correct'] + topic_analysis[topic]['incorrect'])) * 100 if topic_analysis[topic]['correct'] + topic_analysis[topic]['incorrect'] > 0 else 0
#         }
#         for topic in topic_analysis
#     ]

#     topic_labels = json.dumps([topic['topic'] for topic in topic_summary])
#     percentage_data = json.dumps([topic['percentage'] for topic in topic_summary])

#     students_data = sorted(students_data, key=lambda x: x['total_score'], reverse=True)
#     topic_summary = sorted(topic_summary, key=lambda x: x['percentage'], reverse=True)

#     form = StudentAttendanceSearchForm()

#     context = {
#         "form": form,
#         'cbt_category': cbt_category,
#         'students_data': students_data,
#         'topic_summary': topic_summary,
#         "topic_labels": topic_labels,
#         "percentage_data": percentage_data
#     }

#     return render(request, "techsupport/pages/viewCBTAnalysis.html", context=context)


@login_required(login_url="base:home")
def viewCBTAnalysis(request, cbtCategoryId):
    cbt_category = CBTCategory.objects.defer(
                "created_by", "supervisor", "exam_date", "start_time",
                "end_time", "duration", "published"
            ).select_related(
                "assigned_class", "assigned_class__name", "assigned_class__section", 
            ).filter(id=cbtCategoryId).first()
    exams = CBTExam.objects.defer("assigned_class").select_related(
        "session", 
        "cbt_category", "subject", "supervisor", "created_by", "teacher"
    ).prefetch_related("cbt_questions").filter(cbt_category=cbt_category)

    school_branch = request.GET.get("school_branch")
    logger.debug(f"School BRanch: {school_branch}")
    
    # Retrieve all CBTResults for this category at once
    if school_branch:
        student_results = CBTResult.objects.select_related(
                "student", "cbt_category", "cbt_exam"
            ).filter(cbt_category=cbt_category, student__school_branch=school_branch)
    else:
        student_results = CBTResult.objects.select_related(
                "student", "student__user", "student__school_branch", "student__school_branch__manager",
                "cbt_category", "cbt_exam", "cbt_exam__subject"
            ).filter(cbt_category=cbt_category)

    
    students_data = []
    topic_analysis = {}

    for result in student_results:
        student_data = {
            'student': result.student,
            'total_score': 0,
            'correct_answers': 0,
            'incorrect_answers': 0,
            'exam_scores': []  # List to hold scores and percentages per exam
        }
        
        for exam in exams:
            questions = Question.objects.defer("exam", "exam_practice",).select_related(
                                        "subject", "subject__created_by", "topic", "topic__subject", 
                                        "topic__created_by", "topic__subject__created_by", "created_by"
                                    ).prefetch_related(
                                        Prefetch(
                                            'options',
                                            queryset=Option.objects.filter(is_correct=True),
                                            to_attr='correct_option_list'
                                        ), "cbt"
                                    ).filter(cbt=exam)
            student_answers = result.answers.get(str(exam.id), {})
            
            exam_correct_answers = 0
            exam_incorrect_answers = 0

            for question in questions:
                correct_option = question.options.filter(is_correct=True).first()
                
                student_answer = student_answers.get(str(question.id))
                selected_option = question.options.filter(id=student_answer.get('selected')).first() if student_answer else None
                
                if selected_option == correct_option:
                    exam_correct_answers += 1
                    # Update topic analysis for correct answer
                    topic = question.topic
                    if topic:
                        topic_analysis[topic.name] = topic_analysis.get(topic.name, {'correct': 0, 'incorrect': 0, 'subject': topic.subject.name})
                        topic_analysis[topic.name]['correct'] += 1
                else:
                    exam_incorrect_answers += 1
                    # Update topic analysis for incorrect answer
                    topic = question.topic
                    if topic:
                        topic_analysis[topic.name] = topic_analysis.get(topic.name, {'correct': 0, 'incorrect': 0, 'subject': topic.subject.name})
                        topic_analysis[topic.name]['incorrect'] += 1

            exam_score = (exam_correct_answers / questions.count() * 100) if questions.count() > 0 else 0
            student_data['total_score'] += exam_score
            student_data['correct_answers'] += exam_correct_answers
            student_data['incorrect_answers'] += exam_incorrect_answers

            # Append each exam’s score and percentage for this student
            student_data['exam_scores'].append({
                'exam': exam,
                'correct_answers': exam_correct_answers,
                'incorrect_answers': exam_incorrect_answers,
                'score_percentage': exam_score
            })

        # Calculate the total score percentage across all exams for this student
        student_data['total_score'] = student_data['total_score'] / len(exams) if exams else 0
        students_data.append(student_data)

    # Calculate total percentage for each topic in the category
    topic_summary = [
        {
            'topic': topic,
            'subject': topic_analysis[topic]['subject'],
            'correct': topic_analysis[topic]['correct'],
            'incorrect': topic_analysis[topic]['incorrect'],
            'total': topic_analysis[topic]['correct'] + topic_analysis[topic]['incorrect'],
            'percentage': (topic_analysis[topic]['correct'] / (topic_analysis[topic]['correct'] + topic_analysis[topic]['incorrect'])) * 100 if topic_analysis[topic]['correct'] + topic_analysis[topic]['incorrect'] > 0 else 0
        }
        for topic in topic_analysis
    ]

    topic_labels = [topic['topic'] for topic in topic_summary]
    percentage_data = [topic['percentage'] for topic in topic_summary]

    topic_labels = json.dumps(topic_labels)
    percentage_data = json.dumps(percentage_data)

    # Sort student performance by total_score in descending order
    students_data = sorted(students_data, key=lambda x: x['total_score'], reverse=True)

    # Sort topic analysis by percentage in descending order
    topic_summary = sorted(topic_summary, key=lambda x: x['percentage'], reverse=True)

    form = StudentAttendanceSearchForm()

    context = {
        "form": form,
        'cbt_category': cbt_category,
        'students_data': students_data,
        'topic_summary': topic_summary,
        "topic_labels": topic_labels,
        "percentage_data": percentage_data
    }

    return render(request, "techsupport/pages/viewCBTAnalysis.html", context=context)


@login_required(login_url="base:home")
def studentPerformanceAnalysis(request):

    context = {}
    return render(request, "techsupport/pages/studentPerformanceAnalysis.html", context=context)



@login_required(login_url="base:home")
def previewCBTResults(request):
    cbt_results = None
    search_input = request.GET.get("q", " ").strip()

    if search_input:
        cbt_results = CBTResult.objects.only("student", "cbt_category").select_related(
                    "student", "cbt_category"
                ).filter(
                    Q(student__user__username=search_input) | Q(student__registration_number=search_input) |
                    Q(student__school_branch__name=search_input) | Q(student__user__email=search_input)
                )
    else:
        cbt_results = CBTResult.objects.only("student", "cbt_category").select_related("student", "cbt_category").all()

    students = [cbt_result.student for cbt_result in cbt_results]

    context = {"cbt_results": cbt_results, "students": students}
    return render(request, "techsupport/pages/previewCBTResults.html", context=context)


@login_required(login_url="base:home")
def publishCBTResults(request, cbtCategoryId):
    cbt_category = CBTCategory.objects.get(id=cbtCategoryId)

    cbt_results = CBTResult.objects.select_related(
                        "student", "cbt_category", "cbt_exam"
                    ).filter(cbt_category=cbt_category)
    
    if cbt_results.first().published == True:
        for cbt_result in cbt_results:
            cbt_result.published = False
            cbt_result.save()
        messages.success(request, f"CBT results has been unpublished.".capitalize())
    else:
        for cbt_result in cbt_results:
            cbt_result.published = True
            cbt_result.save()
        messages.success(request, f"CBT results has been published.".capitalize())

    return redirect("techsupport:previewCBTCategory")




