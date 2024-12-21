import json
import logging
import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import logout

from base.models import Session, StudentProfile, CustomUser, Subject, Class, SchoolBranch
from attendance.models import StudentAttendance
from examination.models import (Exam, Question, Option, Result, StudentAnswer, 
                                CBTCategory, CBTExam, CBTResult, StudentCBTAnswer
                            )

from utilities import customFuncs, customVars


CURRENT_SESSION = customFuncs.getCurrentSession(Session)
logger = logging.getLogger(__name__)


# Create your views here.
@login_required(login_url="base:home")
def dashboard(request):
    student = request.user.studentprofile
    logger.debug(f"Branch: {student.school_branch}")
    participants = StudentProfile.objects.filter(
                    classes=student.classes, school_branch=student.school_branch
                    ).select_related(
                    "user", "classes", "course", "school_branch"
                    )

    
    student_attendance_summary = StudentAttendance.getStudentAttendanceSummary(student=student,
                                                                                current_session=CURRENT_SESSION
                                                                            )
    student_attendance = StudentAttendance.objects.filter(student=student).order_by("date")

    student_class = Class.objects.filter(name=student.classes.name, 
                                section=student.classes.section
                                ).select_related(
                                    "name", "section"
                                ).prefetch_related(
                                    "subjects"
                                ).first()
    subjects = student_class.subjects.all()

    branches = SchoolBranch.objects.select_related("manager").all()

    # available_exams = Exam.objects.filter(assigned_class=student.classes.name, session=CURRENT_SESSION).all()
    available_exams = CBTCategory.objects.select_related(
                                        "assigned_class", "supervisor", "created_by", "session" 
                                    ).prefetch_related(
                                        "school_branch"
                                    ).filter(
                                        school_branch=student.school_branch,
                                        assigned_class=student.classes, 
                                        session=CURRENT_SESSION,
                                        published=True
                                    )
    # Prepare the data for the chart
    dates = [attendance.date.strftime("%Y-%m-%d") for attendance in student_attendance]
    statuses = [attendance.status for attendance in student_attendance]

    context = {
            "students": participants, 
            "subjects": subjects, 
            "student_class": student_class,
            "branches": branches,
            "available_exams": available_exams,
        }
    return render(request, "./student/pages/dashboard.html", context=context)


@login_required(login_url="base:home")
def viewAttendance(request):
    student = request.user.studentprofile
    student_attendance_summary = StudentAttendance.getStudentAttendanceSummary(student=student,
                                                                                current_session=CURRENT_SESSION
                                                                            )
    student_attendance = StudentAttendance.objects.filter(student=student).order_by("date")
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
            "student_attendance_summary": student_attendance_summary,
            "student_attendance": student_attendance,
            "dates": json.dumps(dates),  # Convert Python list to JSON string,
            "status_values": json.dumps(status_values)  # Convert Python list to JSON string
        }
    return render(request, "./student/pages/viewAttendance.html", context=context)


@login_required(login_url="base:home")
def viewClass(request):
    student = request.user.studentprofile
    class_participants = StudentProfile.objects.filter(classes=student.classes, session=student.session,
                                                school_branch=student.school_branch
                                                ).select_related(
                                                    "user", "classes__name", "session",
                                                    "school_branch__manager", "course"
                                                ).all()
    teachers = student.classes.teachers.all() 
    student_teachers = [teacher for teacher in teachers if teacher.school_branch == student.school_branch]
    male_students_count = class_participants.filter(gender="Male").count()
    female_students_count = class_participants.filter(gender="Female").count()

    context = {
            "class_participants": class_participants, 
            "teachers": student_teachers,
            "male_count": male_students_count,
            "female_count": female_students_count,
        }
    return render(request, "./student/pages/viewClass.html", context=context)


@login_required(login_url="base:home")
def viewParent(request):
    student = request.user
    student_profile = student.studentprofile
    parent_profile = student_profile.parent
    parent = parent_profile.user
    children = parent_profile.children.all()

    context = {
        "parent": parent, "parent_profile": parent_profile, 
        "children": children, "student": student, 
        "student_profile": student_profile,
    }

    return render(request, "./student/pages/viewParent.html", context=context)


@login_required(login_url="base:home")
def viewExamination(request):
    search_input = request.GET.get("q")

    student = request.user.studentprofile
    student_class_subjects = student.classes.subjects.all()
    logger.debug(f"Subjects: {student_class_subjects}")

    # student_exams = Exam.objects.filter(assigned_class=request.user.studentprofile.classes.name).select_related(
    #     "session", "course", "subject", "teacher", "supervisor", "created_by"
    # ).all().order_by("year") 

    student_exams = Exam.objects.filter(
        Q(subject=student_class_subjects[0]) | Q(subject=student_class_subjects[1]) | 
        Q(subject=student_class_subjects[2]) | Q(subject=student_class_subjects[3]),
        published=True
    ).order_by("subject__name").all()


    exam_results = Result.objects.select_related(
        "student__user", "exam"
    ).filter(student=student).all()

    taken_exam_ids = exam_results.values_list('exam_id', flat=True)
    
    # Prepare the data for Chart.js
    exam_labels = [result.exam.subject.name for result in exam_results]  # Exam names
    exam_scores = [result.score for result in exam_results]  # Exam scores

    exam_labels_json = json.dumps(exam_labels)
    exam_scores_json = json.dumps(exam_scores)


    if search_input:
        student_exams = student_exams.filter(
            Q(subject__name__icontains=search_input) | Q(year__icontains=search_input),
        )

    context = {
                "exams": student_exams, 
                "exam_results": exam_results, 
                "taken_exam_ids": taken_exam_ids,
                "exam_labels_json": exam_labels_json,
                "exam_scores_json": exam_scores_json,
            }
    return render(request, "./student/pages/viewExamination.html", context=context)


@login_required(login_url="base:home")
def takeExamination(request, examId):
    exam = get_object_or_404(Exam, id=examId)
    questions = exam.questions.all()
    total_questions = questions.count()

    # Add correct_answer to each question
        # Fetch the correct answer for each question
    for question in questions:
        question.correct_answer = question.options.filter(is_correct=True).first()

    # Convert exam duration to total seconds
    if isinstance(exam.duration, timezone.timedelta):
        duration_seconds = int(exam.duration.total_seconds())
    else:
        duration_seconds = int(exam.duration)  # Assuming duration is stored in seconds

    if request.method == 'POST':
        student = request.user.studentprofile
        questions = Question.objects.filter(exam=exam)

        # Iterate through the submitted answers and save each one
        logger.info(f"Recording and Creating Student Answer For {exam.getExamName}...")
        for index, question in enumerate(questions, start=1):
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = Option.objects.get(id=selected_option_id)

                # Save the student's answer
                StudentAnswer.objects.create(
                    student=student,
                    exam=exam,
                    question=question,
                    selected_option=selected_option
                )
            logger.info(f"Student Answer For {index} - {exam.getExamName} created.")
        logger.info(f"Recording Complete. Student Answer For {exam.getExamName} created.")
        messages.success(request, f"{exam.getExamName} Has Been Submitted.")
        return redirect('student:examResult', examId=exam.id)
    
    context = {
        "exam": exam,
        "questions": questions,
        "total_questions": total_questions,
        "option_labels": customVars.OPTION_LABELS,
        "duration_seconds": duration_seconds
    }

    return render(request, "./student/pages/takeExamination.html", context=context)


@login_required(login_url="base:home")
def examResult(request, examId):
    student = request.user.studentprofile
    exam = Exam.objects.select_related(
        "session", "course", "subject", "supervisor",
        "teacher", "created_by"
    ).get(id=examId)
    questions = Question.objects.defer(
                                    "cbt", "exam_practice"
                                ).select_related(
                                    "subject", "topic", "created_by"
                                ).prefetch_related(
                                    "exam"
                                ).filter(exam=exam).all()
    student_answers = StudentAnswer.objects.filter(exam=exam, student=student).all()

    # Prepare data for the result view
    results = []
    total_questions = questions.count()
    correct_count = 0

    # Loop through each question and evaluate the student's answer
    for question in questions:
        # Get the student's selected option for the current question
        student_answer = student_answers.filter(question=question).first()

        # Get the correct option (assuming 'is_correct' field identifies the correct option)
        correct_option = question.options.filter(is_correct=True).first()

        # Check if the student's answer matches the correct one
        is_correct = (student_answer and student_answer.selected_option == correct_option)
        if is_correct:
            correct_count += 1

        # Append result for this question
        results.append({
            'question': question,
            'selected_option': student_answer.selected_option if student_answer else None,
            'correct_option': correct_option,
            'is_correct': is_correct
        })
    
    # Calculate the score (assuming a simple percentage-based score)
    score = (correct_count / total_questions) * 100 if total_questions > 0 else 0

    result_exist = Result.objects.select_related(
                                        "exam", "student"
                                    ).filter(student=student, exam=exam, 
                                        score=correct_count, score_percentage=score
                                    ).exists()
    if result_exist:
        logger.info(f"{exam.getExamName} Result Already Exists.")
        pass
    else:
        Result.objects.create(
            student=student,
            exam=exam,
            score=correct_count,
            score_percentage=score,
        )
        logger.info(f"{exam.getExamName} Result Created.")


    context = {
            'exam': exam, 
            'results': results,
            "student_answers": student_answers,
            "score": score,
            'correct_count': correct_count,
            'total_questions': total_questions,
            "option_labels": customVars.OPTION_LABELS,
        }
    return render(request, "./student/pages/examResult.html", context=context)


@login_required(login_url="base:home")
def viewCBTExamination(request):
    student_profile = request.user.studentprofile

    # cbt_categories = CBTCategory.objects.select_related(
    #             "assigned_class", "created_by", 
    #             "supervisor", "session"
    #         ).filter(
    #             published=True, assigned_class=student_profile.classes
    #         ).all()
    
    cbt_categories = CBTCategory.objects.select_related(
                                        "assigned_class", "supervisor", "created_by", "session" 
                                    ).prefetch_related(
                                        "school_branch"
                                    ).filter(
                                        school_branch=student_profile.school_branch,
                                        assigned_class=student_profile.classes,
                                        published=True
                                    )

    cbt_results = CBTResult.objects.defer(
                "total_questions", "correct_answers", 
                "incorrect_answers", "skipped_answers"
            ).select_related(
                "student", "cbt_category", "cbt_exam"
            ).filter(
                student=student_profile,
                published=True
            )

    context = {"cbt_categories": cbt_categories, "cbt_results": cbt_results}
    return render(request, "student/pages/viewCBTExamination.html", context=context)


@login_required(login_url="base:home")
def viewCBTExaminationInstruction(request, cbtCategoryId):
    student_profile = request.user.studentprofile
    cbt_category = CBTCategory.objects.get(id=cbtCategoryId)
    student_cbt_result = CBTResult.objects.only("student", "cbt_category"
                                            ).filter(student=student_profile, cbt_category=cbt_category
                                            ).exists()
    
    if student_cbt_result:
        messages.info(request, f"Opps... You have already taken this CBT examination.")
        return redirect("student:viewCBTExamination")

    context = {"cbt_category": cbt_category}
    return render(request, "student/pages/viewCBTExaminationInstruction.html", context=context)


@login_required(login_url="base:home")
def takeCBTExamination(request, cbtCategoryId):
    student_profile = request.user.studentprofile
    timer_end = None
    cbt_category = get_object_or_404(CBTCategory, id=cbtCategoryId)
    exams = CBTExam.objects.filter(cbt_category=cbt_category)

    student_cbt_result = CBTResult.objects.only("student", "cbt_category"
                                            ).filter(student=student_profile, cbt_category=cbt_category
                                            ).exists()
    
    if student_cbt_result:
        messages.info(request, f"Opps... You have already taken this CBT examination.")
        return redirect("student:viewCBTExamination")
    
    all_questions = []
    for exam in exams:
        questions = Question.objects.defer("exam", "exam_practice").filter(cbt=exam).order_by('id')
        all_questions.extend(questions)

    # Set up the timer based on cbt_category duration
    if isinstance(cbt_category.duration, datetime.timedelta):
        timer_end = timezone.now() + cbt_category.duration
    else:
        timer_end = timezone.now() + datetime.timedelta(minutes=cbt_category.duration)

    now = timezone.now()
    duration = (timer_end - now).total_seconds()

    if request.method == 'POST':
        results = {}

        for exam in exams:
            exam_score = 0
            answered_questions = {}
            exam_questions = Question.objects.filter(cbt=exam)

            for question in exam_questions:
                selected_option_id = request.POST.get(f"question_{question.id}")
                if selected_option_id:
                    try:
                        selected_option = Option.objects.get(id=selected_option_id, question=question)
                    except Option.DoesNotExist:
                        # Handle invalid option selection
                        selected_option = None

                    if selected_option and selected_option.is_correct:
                        exam_score += 1

                    correct_option = question.options.filter(is_correct=True).first()

                    answered_questions[str(question.id)] = {
                        'selected': str(selected_option.id) if selected_option else None,
                        'correct': str(correct_option.id) if correct_option else None,
                        'explanation': question.explanation,
                        'topic': question.topic.name if question.topic else "N/A"
                    }

            num_questions = exam_questions.count()
            exam_percentage = (exam_score / num_questions * 100) if num_questions > 0 else 0

            results[str(exam.id)] = {  # Convert exam.id to str
                'score': exam_score,
                'percentage': exam_percentage,
                'questions': answered_questions
            }

        total_score = sum(result['score'] for result in results.values())
        total_percentage_score = (total_score / len(exams) * 100) if exams.count() > 0 else 0

        # Save result with detailed information
        CBTResult.objects.create(
            student=student_profile,
            cbt_category=cbt_category,
            score=total_score,
            score_percentage=total_percentage_score,
            per_exam_scores={str(exam_id): res['percentage'] for exam_id, res in results.items()},
            answers={str(exam_id): res['questions'] for exam_id, res in results.items()}
        )

        messages.success(request, f"You examination has been submited successffully.")
        logout(request)
        return redirect("base:home")
        # return redirect('student:cbtExamResult', cbtCategoryId=cbtCategoryId)

    context = {
        'category': cbt_category,
        'questions': all_questions,
        'duration': duration,
        "timer_end": timer_end,
        "option_labels": customVars.OPTION_LABELS,
    }
    return render(request, 'student/pages/takeCBTExamination.html', context)


@login_required(login_url="base:home")
def cbtExamResult(request, cbtCategoryId):
    student_profile = request.user.studentprofile
    cbt_category = get_object_or_404(CBTCategory, id=cbtCategoryId)
    exams = CBTExam.objects.filter(cbt_category=cbt_category)
    
    # Initialize variables for total questions and correct answers
    total_questions = 0
    total_correct_answers = 0
    
    exams_data = []

    for exam in exams:
        # Get all questions for this exam
        questions = Question.objects.defer(
                                        "exam", "exam_practice"
                                    ).select_related(
                                        "subject", "topic", "created_by"
                                    ).prefetch_related(
                                        "cbt"
                                    ).filter(cbt=exam).order_by("id")
        
        # Add to total question count
        total_questions += questions.count()
        
        # Retrieve the student’s answers from CBTResult if available
        cbt_result = CBTResult.objects.filter(student=student_profile, cbt_category=cbt_category).first()
        student_answers = cbt_result.answers.get(str(exam.id), {}) if cbt_result else {}
        
        exam_questions = []
        exam_correct_answers = 0  # Track correct answers per exam
        
        for question in questions:
            # Get the correct option for the question
            correct_option = question.options.filter(is_correct=True).first()
            
            # Check if the student answered this question
            student_answer = student_answers.get(str(question.id))
            selected_option = question.options.filter(id=student_answer['selected']).first() if student_answer else None
            
            # Check if the answer is correct
            is_correct = selected_option == correct_option if selected_option else None
            if is_correct:
                exam_correct_answers += 1  # Count correct answer per exam
                total_correct_answers += 1  # Count correct answer globally
            
            exam_questions.append({
                'question': question,
                'options': question.options.all(),
                'selected_option': selected_option,
                'correct_option': correct_option,
                'is_correct': is_correct,
                'explanation': question.explanation,
                'topic': question.topic.name if question.topic else "N/A"
            })
        
        exams_data.append({
            'exam': exam,
            'score': (exam_correct_answers / questions.count() * 100) if questions.count() > 0 else 0,
            'questions': exam_questions
        })

    # Calculate total percentage score across all exams
    total_percentage_score = (total_correct_answers / total_questions * 100) if total_questions > 0 else 0

    context = {
        'cbt_category': cbt_category,
        'total_score': total_correct_answers,
        'total_percentage': total_percentage_score,
        'exams_data': exams_data,
        'option_labels': customVars.OPTION_LABELS,
        "total_questions": total_questions
    }
    return render(request, 'student/pages/cbtExamResult.html', context)


@login_required(login_url="base:home")
def viewCBTExamResult(request, cbtCategoryId):
    student_profile = request.user.studentprofile
    cbt_category = get_object_or_404(CBTCategory, id=cbtCategoryId)
    exams = CBTExam.objects.filter(cbt_category=cbt_category)

    # Initialize variables for total questions and correct answers
    total_questions = 0
    total_correct_answers = 0
    
    exams_data = []

    for exam in exams:
        # Get all questions for this exam
        questions = Question.objects.defer(
                                        "exam", "exam_practice"
                                    ).select_related(
                                        "subject", "topic", "created_by"
                                    ).prefetch_related(
                                        "cbt"
                                    ).filter(cbt=exam).order_by("id")
        
        # Add to total question count
        total_questions += questions.count()
        
        # Retrieve the student’s answers from CBTResult if available
        cbt_result = CBTResult.objects.filter(student=student_profile, cbt_category=cbt_category).first()
        student_answers = cbt_result.answers.get(str(exam.id), {}) if cbt_result else {}
        
        exam_questions = []
        exam_correct_answers = 0  # Track correct answers per exam
        
        for question in questions:
            # Get the correct option for the question
            correct_option = question.options.filter(is_correct=True).first()
            
            # Check if the student answered this question
            student_answer = student_answers.get(str(question.id))
            selected_option = question.options.filter(id=student_answer['selected']).first() if student_answer else None
            
            # Check if the answer is correct
            is_correct = selected_option == correct_option if selected_option else None
            if is_correct:
                exam_correct_answers += 1  # Count correct answer per exam
                total_correct_answers += 1  # Count correct answer globally
            
            exam_questions.append({
                'question': question,
                'options': question.options.all(),
                'selected_option': selected_option,
                'correct_option': correct_option,
                'is_correct': is_correct,
                'explanation': question.explanation,
                'topic': question.topic.name if question.topic else "N/A"
            })
        
        exams_data.append({
            'exam': exam,
            'score': (exam_correct_answers / questions.count() * 100) if questions.count() > 0 else 0,
            'questions': exam_questions
        })

    # Calculate total percentage score across all exams
    total_percentage_score = (total_correct_answers / total_questions * 100) if total_questions > 0 else 0

    context = {
        'cbt_category': cbt_category,
        'total_score': total_correct_answers,
        'total_percentage': total_percentage_score,
        'exams_data': exams_data,
        'option_labels': customVars.OPTION_LABELS,
        "total_questions": total_questions
    }
    return render(request, 'student/pages/viewCBTExamResult.html', context)



