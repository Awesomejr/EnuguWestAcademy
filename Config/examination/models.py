import datetime
from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField

from base.models import (TimeStamp, TeacherProfile, StudentProfile, CustomUser, 
                        Course, Session, Subject, Topic, Class, ClassName, SchoolBranch
                        )
from utilities import customVars

# Create your models here.
SLICE_INDEX: int = 20

def examQuestionImagePath(instance, filename):
    return f"examQuestions/{instance.id or instance.pk}_{instance.exam}/{filename}"


def examOptionImagePath(instance, filename):
    return f"examOptions/{instance.id or instance.pk}_{instance.question}/{filename}"


class Exam(TimeStamp):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    assigned_class = models.ForeignKey(ClassName, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    year = models.CharField(max_length=4,  default=str(timezone.now().year))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    instruction = models.CharField(max_length=100, default="Answer All Questions")
    total_marks = models.PositiveIntegerField(default=100, null=False)
    duration = models.DurationField(null=False, default=datetime.timedelta(minutes=50))  # Set time duration for exam
    start_time = models.TimeField(default=timezone.now, null=True, blank=True)
    end_time = models.TimeField(default=timezone.now, null=True, blank=True)
    exam_date = models.DateField(default=timezone.now)
    published = models.BooleanField(default=False)

    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, null=True, blank=True)
    supervisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                    limit_choices_to={'role__in': ["teacher", "tech_support", "mini_tech_support", "superuser"]},
                                    related_name="supervisor"    
                                )
    created_by = models.ForeignKey(CustomUser, null=True,
                                    limit_choices_to={'role__in': ["teacher", "tech_support", "mini_tech_support", "superuser"]}, on_delete=models.CASCADE, related_name="created_exams",
                                )

    class Meta:
        ordering = ("-created_on",)

    def __str__(self):
        return f"Exam: {self.subject} - {self.year}"
    

    @property
    def getExamName(self):
        return f"{self.subject}-{self.year}"

    # logic to increment question number
    # def save(self, *args, **kwargs):
    # if self.number == 0:
    #     self.number = self.exam.questions.count() + 1
    # super().save(*args, **kwargs)


class CBTCategory(TimeStamp):
    school_branch = models.ManyToManyField(SchoolBranch, null=True, blank=True, related_name="cbt_categrories")
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, 
                                        blank=True, related_name="cbt_categories"
                                    )
    number_of_subject = models.IntegerField(default=4, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(max_length=100, default="")
    exam_date = models.DateField(default=timezone.now, null=True, blank=True)
    start_time = models.TimeField(default=timezone.now, null=True, blank=True)
    end_time = models.TimeField(default=timezone.now, null=True, blank=True)
    duration = models.DurationField(null=False, default=datetime.timedelta(minutes=120))  # Set time duration for exam
    published = models.BooleanField(default=False)

    supervisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                    limit_choices_to={'role__in': ["teacher", "tech_support", "mini_tech_support", "superuser"]},
                                    related_name="cbt_supervisor"    
                                )
    created_by = models.ForeignKey(CustomUser, null=True, blank=True, 
                                    limit_choices_to={'role__in': ["teacher", "tech_support", "mini_tech_support", "superuser"]}, on_delete=models.CASCADE, related_name="created_cbt_categories",
                                )
    
    class Meta:
        ordering = ("-created_on",)

    
    def __str__(self):
        return f"CBT: {self.exam_date} {self.assigned_class.getClassName}-{self.description[:30]}"
    
    @property
    def getCBTName(self):
        return f"{self.description} for {self.assigned_class.getClassName}"


class CBTExam(TimeStamp):
    cbt_category = models.ForeignKey(CBTCategory, on_delete=models.CASCADE, null=True, blank=True, related_name="exams")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="cbt_exams")
    year = models.CharField(max_length=4,  default=str(timezone.now().year))
    duration = models.DurationField(null=False, default=datetime.timedelta(minutes=120))  # Set time duration for exam
    start_time = models.TimeField(default=timezone.now, null=True, blank=True)
    end_time = models.TimeField(default=timezone.now, null=True, blank=True)
    exam_date = models.DateField(default=timezone.now)

    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, null=True, blank=True)
    supervisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                limit_choices_to={'role__in': ["teacher", "tech_support", "mini_tech_support", "superuser"]},
                                related_name="cbt_exam_supervisor"    
                                )
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_cbt_exams",
                                limit_choices_to={'role__in': ["teacher", "tech_support", "mini_tech_support", "superuser"]}, 
                                null=True,
                            )
    class Meta:
        ordering = ("-created_on",)


    def __str__(self):
        return f"Exam: {self.subject} - {self.session}"
    

    @property
    def getExamName(self):
        return f"{self.subject}-{self.year}-{self.session.getSessionName}"


class ExamPracticeCategory(TimeStamp):
    assigned_class = models.ForeignKey(ClassName, on_delete=models.CASCADE, null=True, blank=True, related_name="exam_practice_categories")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_exam_practice_categories",
                                limit_choices_to={'role__in': ["teacher", "tech_support", "mini_tech_support", "superuser"]}, 
                                null=True,
                            )

    class Meta:
        ordering = ("-created_on",)
    
    def __str__(self):
        return f"CBT: {self.assigned_class}-{self.session.getSessionName}"
    

class ExamPractice(TimeStamp):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    number_of_subject = models.IntegerField(default=4, null=True, blank=True)
    assigned_class = models.ForeignKey(ClassName, on_delete=models.CASCADE, null=True, blank=True)
    exam_practice_category = models.ForeignKey(ExamPracticeCategory, on_delete=models.CASCADE, null=True, blank=True, related_name="exams")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="exam_practices")
    year = models.CharField(max_length=4,  default=str(timezone.now().year))
    duration = models.DurationField(null=False, default=datetime.timedelta(minutes=120))  # Set time duration for exam
    start_time = models.TimeField(default=timezone.now, null=True, blank=True)
    end_time = models.TimeField(default=timezone.now, null=True, blank=True)
    exam_date = models.DateField(default=timezone.now)

    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, null=True, blank=True)
    supervisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                    limit_choices_to={'role__in': ["teacher", "tech_support", "mini_tech_support", "superuser"]},
                                    related_name="exam_practice_supervisor"    
                                )
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_exam_practices", null=True,
                                limit_choices_to={'role__in': ["teacher", "tech_support", "mini_tech_support", "superuser"]}, 
                                )
    
    class Meta:
        ordering = ("-created_on",)
    
    def __str__(self):
        return f"Exam: {self.subject} - {self.session}"
    

    @property
    def getExamName(self):
        return f"{self.subject}-{self.year}-{self.session.getSessionName}"



class Question(TimeStamp):
    exam = models.ManyToManyField(Exam, blank=True, related_name="questions")
    cbt = models.ManyToManyField(CBTExam, blank=True, related_name="cbt_questions")
    exam_practice = models.ManyToManyField(ExamPractice, blank=True, related_name="exam_practice_questions"
                                    )

    question_type = models.CharField(max_length=50, choices=customVars.QUESTION_TYPE, default="Past-Question")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    year = models.CharField(max_length=4,  default=str(timezone.now().year))
    number = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to=examQuestionImagePath, null=True, blank=True) # Question can be an image
    # title = RichTextField(null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    explanation = RichTextField(max_length=1000, null=True, blank=True)
    mark = models.SmallIntegerField(default=2, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.CharField(max_length=20, default="Normal", choices=customVars.QUESTION_DIFFICULTY)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_questions",  null=True,
                                limit_choices_to={'role__in': ["teacher", "tech_support", "mini_tech_support", "superuser", "manager", "academic_director"]}, 
                                )
    
    class Meta:
        ordering = ("-created_on",)

    def __str__(self):
        return f"Question: {self.subject} {self.content[:20]}"
    
    # @property
    # def getQuestionName(self):
    #     return f"{self.topic.name} - {self.content[:10]}"



class Option(TimeStamp):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    content = RichTextField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to=examOptionImagePath, null=True, blank=True) # Option can be an image
    is_correct = models.BooleanField(default=False)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_options", null=True,
                                limit_choices_to={'role__in': ["teacher", "tech_support", "mini_tech_support", "superuser"]}, 
                                )
    
    class Meta:
        ordering = ("-created_on",)

    def __str__(self):
        return f"Option: {self.content}"
    

################################################ CBT ###########################################################

class StudentCBTAnswer(TimeStamp):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="cbt_answers")
    cbt_category = models.ForeignKey(CBTCategory, on_delete=models.CASCADE, null=True, blank=True)
    cbt_exam = models.ForeignKey(CBTExam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        # unique_together = ('student', 'question')  # Prevent multiple answers for the same question by the same student
        ordering = ("-created_on",)

    def __str__(self):
        return f"{self.student.user.getFullName}'s answer for {self.question.content}"
    

class CBTResult(TimeStamp):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="student_cbt_results")
    cbt_category = models.ForeignKey(CBTCategory, on_delete=models.CASCADE, null=True, blank=True)
    cbt_exam = models.ForeignKey(CBTExam, on_delete=models.CASCADE, related_name="cbt_exam_results", null=True, blank=True)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)
    skipped_answers = models.IntegerField(default=0)
    score = models.FloatField(default=0)
    score_percentage = models.FloatField(null=True, blank=True)  # Optional: Store percentage
    # New fields
    per_exam_scores = models.JSONField(default=dict, blank=True)  # Store scores for each exam in the category
    answers = models.JSONField(default=dict, blank=True)  # Store detailed answers for each question
    published = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     if self.exam.total_marks:
    #         self.score_percentage = (self.score / self.exam.total_marks) * 100
    #     super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_on",)

    def __str__(self):
        return f"CBT Result: {self.student.user.getFullName} - {self.cbt_exam} - {self.score}"
    # ...



































class StudentAnswer(TimeStamp):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="exam_answers")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        # unique_together = ('student', 'question')  # Prevent multiple answers for the same question by the same student
        ordering = ("-created_on",)

    def __str__(self):
        return f"{self.student.user.getFullName}'s answer for {self.question.content}"


class Result(TimeStamp):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="results")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="results")
    score = models.FloatField()
    score_percentage = models.FloatField(null=True, blank=True)  # Optional: Store percentage

    # def save(self, *args, **kwargs):
    #     if self.exam.total_marks:
    #         self.score_percentage = (self.score / self.exam.total_marks) * 100
    #     super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_on",)

    def __str__(self):
        return f"Result: {self.student.user.getFullName} - {self.exam} - {self.score}"