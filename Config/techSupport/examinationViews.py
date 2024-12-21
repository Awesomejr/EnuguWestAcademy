import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

from base.models import Topic
from examination.models import Exam, Question, Option
from .forms import (CreateExamForm, CreateExamQuestionForm, OptionFormSet, EditExamQuestionForm)
from utilities import customFuncs, customVars


logger = logging.getLogger(__name__)


@login_required(login_url="base:home")
def createExamination(request):
    if request.method == "POST":
        form = CreateExamForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get("subject")
            exam = form.save(commit=False)
            exam.created_by = request.user
            exam.save()

            logger.info(f"Exam '{subject.name}' has been created.")
            messages.success(request, f"Exam '{subject.name}' has been created.")
            return redirect("techsupport:createExamination")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateExamForm()

    context={"form": form, "years": [year for year in range(2000, 2031)]}

    return render(request, "techsupport/pages/createExamination.html", context=context)


@login_required(login_url="base:home")
def editExamination(request, examId):
    exam = Exam.objects.filter(id=examId).first()

    if request.method == "POST":
        form = CreateExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            logger.info(f"Exam '{exam.getExamName}' has been updated.".capitalize())
            messages.success(request, f"Exam '{exam.getExamName}' has been updated.".capitalize())
            return redirect("techsupport:previewExamination")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateExamForm(instance=exam)

    context = {"exam": exam, "form":form}
    return render(request, "techsupport/pages/editExamination.html", context=context)



@login_required(login_url="base:home")
def previewExamination(request):
    exams_to_display = None
    filter_input = request.GET.get("filter")
    search_input = request.GET.get("q")

    exams = Exam.objects.select_related(
        "session", "course", "assigned_class", "subject", "teacher", "supervisor", "created_by"
    ).all()

    if search_input:
        exams_to_display = exams.filter(
            Q(subject__name__icontains=search_input) | Q(year__icontains=search_input),
        ).all()
    elif filter_input == "all":
        exams_to_display = exams
    elif filter_input:
        exams_to_display = exams[:int(filter_input)]
    else:
        exams_to_display = exams
    
    paginator = Paginator(exams_to_display, int(customVars.NUMBER_OF_TABLE_ROW))
    page_number = request.GET.get("page")
    exams_page =paginator.get_page(page_number)


    context = {"exams": exams_page}

    if request.htmx:
        return render(request, "exams/components/previewExaminationTable.html", context=context)

    return render(request, "techsupport/pages/previewExamination.html", context=context)


@login_required(login_url="base:home")
def printExamination(request, examId):
    exam = Exam.objects.filter(id=examId).first()
    questions = exam.questions.all().order_by("created_on")
    total_questions = questions.count()
    option_labels = ['A', 'B', 'C', 'D']

    context = {
            "exam": exam, "questions": questions, 
            "total_questions": total_questions, "option_labels": option_labels
        }
    return render(request, "techsupport/pages/printExamination.html", context=context)


@login_required(login_url="base:home")
def createExaminationQuestion(request):
    topic = None
    topics = Topic.objects.select_related("subject").all()
    exams = Exam.objects.select_related(
        "session", "course", "subject", "supervisor", "teacher", "created_by"
    ).all()
    if request.method == "POST":
        question_form = CreateExamQuestionForm(request.POST, request.FILES)
        
        topic_id = request.POST.get("topic")
        exam_id = request.POST.get("exam")
        if topic_id:
            topic = Topic.objects.filter(id=topic_id).first()
        exam = Exam.objects.filter(id=exam_id).first()

        if question_form.is_valid():
            question_image = question_form.cleaned_data.get("image")
            logger.debug(f"Question Image: {question_image}")
            question = question_form.save(commit=False)
            question.exam = exam
            question.topic = topic
            if question_image:
                try:
                    resized_image = customFuncs.resizeImage(question_image)
                    question.image = resized_image
                except:
                    pass
            question.created_by = request.user
            question.save()

            logger.info(f"Question '{question.content}' has been created.")
            messages.success(request, f"Question has been created.")
            return redirect("techsupport:createExaminationQuestionOption", questionId=question.id)
        else:
            customFuncs.displayFormErrors(request, question_form, messages, logger)
    else:
        question_form = CreateExamQuestionForm()

    context = {"question_form": question_form, "topics": topics, "exams":exams}
    return render(request, "techsupport/pages/createExaminationQuestion.html", context=context)


def topicsOptions(request):
    exam_id = request.GET.get("exam")
    exam = Exam.objects.get(id=exam_id)
    topics = exam.subject.topics.all()
    logger.debug(f"Topics: {topics}")
    context = {"topics": topics}
    return render(request, "techsupport/components/topicsOptions.html", context=context)


@login_required(login_url="base:home")
def previewExaminationQuestion(request):
    questions_to_display = None
    search_input = request.GET.get("q")
    filter_input = request.GET.get("filter")

    questions = Question.objects.select_related("exam__subject", "topic").all().order_by("-created_on")

    if search_input:
        questions_to_display = questions.filter(
            Q(content__icontains=search_input) |
            Q(topic__name__icontains=search_input) |
            Q(exam__subject__name__icontains=search_input) |
            Q(cbt__subject__name__icontains=search_input)
        )
    elif filter_input == "all":
        questions_to_display = questions
    elif filter_input:
        questions_to_display = questions[:int(filter_input)]
    else:
        questions_to_display = questions

    paginator = Paginator(questions_to_display, int(customVars.NUMBER_OF_TABLE_ROW))
    page_number = request.GET.get("page")
    questions_page =paginator.get_page(page_number)

    context = {
            # "questions": questions,
            "questions_to_display": questions_page, 
        }
    
    if request.htmx:
        return render(request, "./techsupport/components/previewExaminationQuestionTable.html", context=context)
    
    return render(request, "techsupport/pages/previewExaminationQuestion.html", context=context)


def editExaminationQuestion(request, questionId):   
    question = Question.objects.filter(id=questionId).first()
    if request.method == "POST":
        form = EditExamQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            logger.info(f"Question has been updated.".capitalize())
            messages.success(request, f"Question has been updated.".capitalize())
            return redirect("techsupport:previewExaminationQuestion")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = EditExamQuestionForm(instance=question)

    context = {"form": form, "question": question}
    return render(request, "techsupport/pages/editExaminationQuestion.html", context=context)



@login_required(login_url="base:home")
def createExaminationQuestionOption(request, questionId):
    try:
        question = Question.objects.get(id=questionId)
    except Question.DoesNotExist:
        messages.error(request, "Question not found.")
        return redirect("techsupport:createExaminationQuestion")

    if request.method == "POST":
        # question = request.POST.get("question")
        option_formset = OptionFormSet(request.POST, request.FILES, instance=question)
        if option_formset.is_valid():
            # Use a formset for multiple option instances
            options = option_formset.save(commit=False)
            for option in options:
                option.created_by = request.user
                option.question = question  # Ensure the question is assigned correctly
                option.save()

            logger.info(f"Options for question '{question}' have been created.")
            messages.success(request, f"Options has been created.")
            return redirect("techsupport:createExaminationQuestion")
        else:
            customFuncs.displayFormErrors(request, option_formset, messages, logger)
    else:
        option_formset = OptionFormSet()

    context = {"option_formset": option_formset, "question": question}
    return render(request, "techsupport/pages/createExaminationQuestionOption.html", context=context)


@login_required(login_url="base:home")
def previewExaminationQuestionOption(request):
    options_to_display = None
    filter_input = request.GET.get("filter")
    search_input = request.GET.get("q")
    logger.debug(f"Search: Input {search_input}")
    options = Option.objects.select_related(
            "question", "question__exam", "question__exam__subject"
        ).all()

    if search_input:
        options_to_display = options.filter(content__icontains=search_input).all()
    elif filter_input == "all":
        options_to_display = options
    elif filter_input:
        options_to_display = options[:int(filter_input)]
    else:
        options_to_display = options

    paginator = Paginator(options_to_display, int(customVars.NUMBER_OF_TABLE_ROW))
    page_number = request.GET.get("page")
    options_page =paginator.get_page(page_number)

    context = {
            # "options": options,
            "options_to_display": options_page,
        }
    
    if request.htmx:
        return render(request, "./techsupport/components/previewExaminationQuestionOptionTable.html", context=context)
    return render(request, "techsupport/pages/previewExaminationQuestionOption.html", context=context)


@login_required(login_url="base:home")
def publishExamination(request, examId):
    exam = Exam.objects.filter(id=examId).first()

    customFuncs.objectModificationLog(request, logger, "exam")
    if exam.published == True:
        exam.published = False
        exam.save()
        messages.success(request, f"Exam '{exam.getExamName}' has been made unpublished.".capitalize())
        logger.info(f"Exam '{exam.getExamName}' has been made unpublished.".capitalize())
    else:
        exam.published = True
        exam.save()
        messages.success(request, f"Exam '{exam.getExamName}' has been made published.".capitalize())
        logger.info(f"Exam '{exam.getExamName}' has been made published.".capitalize())

    return redirect("techsupport:previewExamination")