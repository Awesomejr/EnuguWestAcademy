import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from base.models import (Session, Subject, Topic, SchoolBranch, Class, Course, StudentProfile, 
                        CustomUser, TeacherProfile
                    )
from examination.models import Exam, Question, Option, StudentAnswer, Result, CBTCategory, CBTResult
from utilities import customFuncs, customVars


logger = logging.getLogger(__name__)
DELETE_TEMPLATE = "main/pages/deleteConfirmation.html"


@login_required(login_url="base:home")
def deleteStudent(request, studentId):
    student_to_delete = CustomUser.objects.get(id=studentId)
    student_profile = student_to_delete.studentprofile
    parent_profile = student_profile.parent
    parent_to_delete = parent_profile.user
    

    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "student and parent")
        student_to_delete.delete()
        parent_to_delete.delete()
        logger.info("Student and Parent account has been deleted.")
        messages.success(request, "Student and Parent account has been deleted.")
        return redirect("techsupport:viewStudents")
    
    context = {'object_to_delete': student_to_delete}
    return render(request, DELETE_TEMPLATE, context=context)


@login_required(login_url="base:home")
def deleteTeacher(request, teacherId):
    teacher_to_delete = CustomUser.objects.get(id=teacherId)

    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "teacher")
        teacher_to_delete.delete()
        logger.info("Teacher has been deleted.")
        messages.success(request, "Teacher has been deleted.")
        return redirect("techsupport:viewTeachers")
    
    context = {'object_to_delete': teacher_to_delete}
    return render(request, DELETE_TEMPLATE, context=context)


@login_required(login_url="base:home")
def deletePrevillagedUser(request, userId):
    user_to_delete = CustomUser.objects.get(id=userId)

    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "previllaged user")
        user_to_delete.delete()
        logger.info("User has been deleted.")
        messages.success(request, "User has been deleted.")
        return redirect("techsupport:viewPrevillagedUsers")
    
    context = {'object_to_delete': user_to_delete}
    return render(request, DELETE_TEMPLATE, context=context)



@login_required(login_url="base:home")
def deleteSession(request, sessionId):
    session = Session.objects.get(id=sessionId)
    
    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "session")
        session.delete()
        logger.info("Session has been deleted.")
        messages.success(request, "Session has been deleted.")
        return redirect("techsupport:createSession")
    
    context = {'object_to_delete': session}
    return render(request, DELETE_TEMPLATE, context=context)


@login_required(login_url="base:home")
def deleteSubject(request, subjectId):
    subject = Subject.objects.filter(id=subjectId).first()
    
    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "Subject")
        subject.delete()
        logger.info(f"Subject has been deleted.".capitalize())
        messages.success(request, f"Subject has been deleted.".capitalize())
        return redirect("techsupport:createSubject")
    
    context = {'object_to_delete': subject}
    return render(request, DELETE_TEMPLATE, context=context)


@login_required(login_url="base:home")
def deleteTopic(request, topicId):
    topic = Topic.objects.select_related("subject").filter(id=topicId).first()
    
    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "Topic")
        topic.delete()
        logger.info(f"Topic has been deleted.".capitalize())
        messages.success(request, f"Topic has been deleted.".capitalize())
        return redirect("techsupport:createTopic")
    
    context = {'object_to_delete': topic}
    return render(request, DELETE_TEMPLATE, context=context)


@login_required(login_url="base:home")
def deleteSchoolBranch(request, schoolBranchId):
    school_branch = SchoolBranch.objects.select_related("manager").filter(id=schoolBranchId).first()

    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "school branch")
        school_branch.delete()
        logger.info(f"School Branch has been deleted.".capitalize())
        messages.success(request, f"School Branch has been deleted.".capitalize())
        return redirect("techsupport:createSchoolBranch")
    
    context = {'object_to_delete': school_branch}
    return render(request, DELETE_TEMPLATE, context=context)


@login_required(login_url="base:home")
def deleteClass(request, classId):
    class_to_delete = Class.objects.select_related("section", "name").filter(id=classId).first()
    
    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "class")
        class_to_delete.delete()
        logger.info(f"Class has been deleted.".capitalize())
        messages.success(request, f"Class has been deleted.".capitalize())
        return redirect("techsupport:createClass")
    
    context = {'object_to_delete': class_to_delete}
    return render(request, DELETE_TEMPLATE, context=context)


@login_required(login_url="base:home")
def deleteCourse(request, courseId):
    course_to_delete = Course.objects.prefetch_related("subjects").filter(id=courseId).first()
    
    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "course")
        course_to_delete.delete()
        logger.info(f"Course has been deleted.".capitalize())
        messages.success(request, f"Course has been deleted.".capitalize())
        return redirect("techsupport:createCourse")
    
    context = {'object_to_delete': course_to_delete}
    return render(request, DELETE_TEMPLATE, context=context)


@login_required(login_url="base:home")
def deleteExamination(request, examId):
    exam = Exam.objects.select_related("session", "assigned_class", "course", "subject").filter(id=examId).first()
    
    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "exam")
        exam.delete()
        logger.info(f"Exam has been deleted.".capitalize())
        messages.success(request, f"Exam has been deleted.".capitalize())
        return redirect("techsupport:previewExamination")
    
    context = {'object_to_delete': exam}
    return render(request, DELETE_TEMPLATE, context=context)


@login_required(login_url="base:home")
def deleteExaminationQuestion(request, questionId):
    question = Question.objects.select_related("exam", "cbt", "exam_practice", "topic").filter(id=questionId).first()
    
    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "exam_question")
        question.delete()
        logger.info(f"Question has been deleted.".capitalize())
        messages.success(request, f"Question has been deleted.".capitalize())
        return redirect("techsupport:previewExaminationQuestion")
    
    context = {'object_to_delete': question}
    return render(request, DELETE_TEMPLATE, context=context)


@login_required(login_url="base:home")
def deleteQuestion(request, questionId):
    question = Question.objects.defer("exam", "cbt", "exam_practice").select_related("topic").filter(id=questionId).first()

    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "question")
        question.delete()
        logger.info(f"Question has been deleted.".capitalize())
        messages.success(request, f"Question has been deleted.".capitalize())
        return redirect("techsupport:viewQuestions")

    context = {'object_to_delete': question}
    return render(request, DELETE_TEMPLATE, context=context)


@login_required(login_url="base:home")
def deleteCBTCategory(request, cbtCategoryId):
    cbt_category = CBTCategory.objects.get(id=cbtCategoryId)

    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, "cbt category")
        cbt_category.delete()
        logger.info(f"CBT Category has been deleted.".capitalize())
        messages.success(request, f"CBT Category has been deleted.".capitalize())
        return redirect("techsupport:previewCBTCategory")
    
    context = {'object_to_delete': cbt_category}
    return render(request, DELETE_TEMPLATE, context=context)


@login_required(login_url="base:home")
def deleteCBTResult(request, cbtResultId):
    cbt_result = CBTResult.objects.get(id=cbtResultId)
    if request.method == "POST":
        customFuncs.objectModificationLog(request, logger, f"cbt result for {cbt_result.student.user.getFullName} ")
        cbt_result.delete()
        logger.info(f"CBT Result has been deleted.".capitalize())
        messages.success(request, f"CBT Result has been deleted.".capitalize())
        return redirect("techsupport:previewCBTResults")
    
    context = {'object_to_delete': cbt_result}
    return render(request, DELETE_TEMPLATE, context=context)

