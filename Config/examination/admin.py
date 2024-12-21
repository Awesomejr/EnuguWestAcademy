from django.contrib import admin

from .models import (Exam, Question, Option, StudentAnswer, Result, CBTCategory, 
                    CBTExam, CBTResult, StudentCBTAnswer, ExamPractice, ExamPracticeCategory
                )


# Register your models here.
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'session',
        'assigned_class',
        'course',
        'year',
        'subject',
        'instruction',
        'total_marks',
        'duration',
        'start_time',
        'end_time',
        'exam_date',
        'published',
        'teacher',
        'supervisor',
        'created_by',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'session',
        'assigned_class',
        'course',
        'subject',
        'exam_date',
        'published',
        'teacher',
        'supervisor',
        'created_by',
    )


@admin.register(CBTCategory)
class CBTCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'assigned_class',
        'number_of_subject',
        'session',
        'description',
        'exam_date',
        'start_time',
        'end_time',
        'duration',
        'published',
        'supervisor',
        'created_by',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'assigned_class',
        'session',
        'exam_date',
        'published',
        'supervisor',
        'created_by',
    )


@admin.register(CBTExam)
class CBTExamAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'cbt_category',
        'session',
        'assigned_class',
        'subject',
        'year',
        'duration',
        'start_time',
        'end_time',
        'exam_date',
        'teacher',
        'supervisor',
        'created_by',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'cbt_category',
        'session',
        'assigned_class',
        'subject',
        'exam_date',
        'teacher',
        'supervisor',
        'created_by',
    )


@admin.register(ExamPracticeCategory)
class ExamPracticeCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'assigned_class',
        'session',
        'created_by',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'assigned_class',
        'session',
        'created_by',
    )


@admin.register(ExamPractice)
class ExamPracticeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'session',
        'number_of_subject',
        'assigned_class',
        'exam_practice_category',
        'subject',
        'year',
        'duration',
        'start_time',
        'end_time',
        'exam_date',
        'teacher',
        'supervisor',
        'created_by',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'session',
        'assigned_class',
        'exam_practice_category',
        'subject',
        'exam_date',
        'teacher',
        'supervisor',
        'created_by',
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        # 'exam',
        # 'cbt',
        # 'exam_practice',
        'question_type',
        'subject',
        'year',
        'number',
        'image',
        'content',
        'explanation',
        'mark',
        'topic',
        'level',
        'created_by',
    )
    list_filter = ('created_on', 'updated_on')
    search_fields = ("id", "content", "topic",)
    # raw_id_fields = (
    #     'exam',
    #     'cbt',
    #     'exam_practice',
    #     'subject',
    #     'topic',
    #     'created_by',
    # )


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'question',
        'content',
        'image',
        'is_correct',
        'created_by',
    )
    list_filter = ('created_on', 'updated_on', 'is_correct')
    raw_id_fields = ('question', 'created_by')


@admin.register(StudentCBTAnswer)
class StudentCBTAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'student',
        'cbt_category',
        'cbt_exam',
        'question',
        'selected_option',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'student',
        'cbt_category',
        'cbt_exam',
        'question',
        'selected_option',
    )


@admin.register(CBTResult)
class CBTResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'student',
        'cbt_category',
        # 'cbt_exam',
        # 'total_questions',
        # 'correct_answers',
        # 'incorrect_answers',
        # 'skipped_answers',
        'score',
        'score_percentage',
        'published',
        # 'per_exam_scores',
        # 'answers',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'student',
        'cbt_category',
        'cbt_exam',
    )


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'student',
        'exam',
        'question',
        'selected_option',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'student',
        'exam',
        'question',
        'selected_option',
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'student',
        'exam',
        'score',
        'score_percentage',
    )
    list_filter = ('created_on', 'updated_on', 'student', 'exam')