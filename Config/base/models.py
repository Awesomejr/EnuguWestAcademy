import datetime
import uuid
import logging

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from utilities.customVars import *
from utilities import customFuncs

# Create your models here.
logger = logging.getLogger(__name__)


def userAvatarPath(instance, filename):
    return f"avatars/{instance.id or instance.pk}_{instance.first_name}_{instance.last_name}_" \
            f"{instance.middle_name}/{filename}"

def teacherCVPath(instance, filename):
    return f"credentials/cv/{instance.id or instance.pk}_{instance.phone_number}/{filename}"


class TimeStamp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_on = models.DateTimeField(auto_now_add=True)  # Corrected
    updated_on = models.DateTimeField(auto_now=True)      # Corrected

    class Meta:
        abstract = True


class BaseProfile(models.Model):
    bio = models.TextField(max_length=500, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=30, choices=COUNTRIES, null=True, blank=True)
    state = models.CharField(max_length=30, choices=STATES, null=True, blank=True)
    local_government_area = models.CharField(max_length=50, null=True, blank=True)
    town = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=50, choices=RELIGION_CHOICES, null=True, blank=True)

    class Meta:
        abstract = True


class Session(TimeStamp):
    session = models.CharField(max_length=15, null=True, help_text="Format: 2024/2025")
    name = models.CharField(max_length=100, null=True, choices=BATCHES)
    start_date = models.DateField(null=False, default=timezone.now)
    closing_date = models.DateField(null=False, default=timezone.now)

    class Meta:
        verbose_name_plural = "School Session"

    def __str__(self):
        return f"Session: {self.name}-{self.session}"
    
    @property
    def getSessionName(self):
        return f"{self.name}-{self.session}"
    

class CustomUser(TimeStamp, AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    avatar = models.ImageField(default="avatars/avatar.svg", upload_to=userAvatarPath, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_suspended = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ("created_on", "first_name", "last_name")
        verbose_name_plural = "Custom Users"

    def __str__(self):
        return f"{self.first_name.capitalize()} " \
                f"{self.last_name.capitalize()} {self.middle_name.capitalize()} - {self.role}"

    @property
    def getFullName(self):
        name = None
        if self.first_name and self.last_name and self.middle_name:
            name = f"{self.first_name}_{self.last_name}_{self.middle_name}"
        elif self.username:
            name = f"ewja/{self.username}"
        else:
            name = f"@{self.email}"

        return name
    
    @property
    def displayAvatar(self):
        user_avatar = None
        if self.avatar.url:
            user_avatar = self.avatar.url
        return user_avatar
    
    @property
    def getAge(self):
        today = timezone.now().date()
        year_difference = int(today.year - (self.date_of_birth.year))
        age = year_difference - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age
    

class SchoolBranch(TimeStamp):
    name = models.CharField(max_length=200)
    manager = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                    limit_choices_to={'role__in': ALLOWED_MODIFICATION_ROLES}
                                )
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, 
                        related_name="created_school_branches", limit_choices_to={'role__in':ALLOWED_MODIFICATION_ROLES}
                    )

    def __str__(self):
        return f"Cluster: {self.name}"


class ParentProfile(TimeStamp, BaseProfile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    custom_user_id = models.UUIDField(null=True)
    school_branch = models.ForeignKey(SchoolBranch, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
    identification_type = models.CharField(max_length=50, choices=IDENTIFICATION_TYPES, blank=True, null=True)
    identification_number = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    father_occupation = models.CharField(max_length=50, null=True, blank=True)
    mother_occupation = models.CharField(max_length=50, null=True, blank=True)
    father_work_address = models.CharField(max_length=200, null=True, blank=True)
    mother_work_address = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    secondary_phone_number = models.CharField(max_length=14, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="parent_profiles", limit_choices_to={'role__in': ALLOWED_MODIFICATION_ROLES})

    def __str__(self):
        return f"Parent Profile: {self.user}- {self.phone_number}"
    

class StudentProfile(TimeStamp, BaseProfile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    custom_user_id = models.UUIDField(null=True)
    parent = models.ForeignKey(ParentProfile, models.SET_NULL, null=True, blank=True, related_name="children")
    admission_year = models.DateField(null=True, blank=True)
    registration_number = models.CharField(max_length=200, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
    school_branch = models.ForeignKey(SchoolBranch, on_delete=models.SET_NULL, null=True, blank=True)
    class_number = models.PositiveIntegerField(null=True, blank=True)
    student_status = models.CharField(max_length=30, choices=STUDENT_STATUS, default="Full-time")
    is_first_child = models.BooleanField(default=False, null=True, blank=True)
    is_last_child = models.BooleanField(default=False, null=True, blank=True)
    current_address = models.CharField(max_length=200, null=True, blank=True)
    permanent_address = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    course = models.ForeignKey("Course", on_delete=models.SET_NULL, null=True, blank=True)
    classes = models.ForeignKey("Class", on_delete=models.SET_NULL, null=True, blank=True)
    previous_school = models.CharField(max_length=200, null=True, blank=True)
    previous_school_date = models.DateField(null=True, blank=True)
    reason_for_leaving = models.TextField(max_length=500, null=True, blank=True)
    any_disability = models.CharField(max_length=5, choices=YES_NO_LIST, null=True, blank=True)
    disability_description = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="student_profiles", limit_choices_to={'role__in': ALLOWED_MODIFICATION_ROLES})

    def __str__(self):
        return f"Student Profile: {self.user}- {self.phone_number}"


class TeacherProfile(TimeStamp, BaseProfile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    custom_user_id = models.UUIDField(null=True)
    school_branch = models.ForeignKey(SchoolBranch, on_delete=models.SET_NULL, null=True, blank=True)
    current_address = models.CharField(max_length=200, null=True, blank=True)
    permanent_address = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    qualification = models.CharField(max_length=10, choices=QUALIFICATIONS, null=True, blank=True)
    cv = models.FileField(upload_to=teacherCVPath, null=True, blank=True)
    relationship = models.CharField(max_length=15, choices=RELATIONSHIPS, null=True)
    any_experience = models.CharField(max_length=5, choices=YES_NO_LIST, default="None", null=True, blank=True)
    experience_description = models.TextField(max_length=500, null=True, blank=True)
    assigned_class = models.ManyToManyField("Class", related_name="teachers")
    teacher_subject = models.ForeignKey("Subject", on_delete=models.SET_NULL, null=True, related_name="teachers")
    teacher_status = models.CharField(max_length=20, choices=TEACHER_STATUS_LIST)
    salary = models.CharField(max_length=10, default=DEFAULT_SALARY, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="teacher_profiles", limit_choices_to={'role__in': ALLOWED_MODIFICATION_ROLES})

    def __str__(self):
        return f"Teacher Profile: {self.user} - {self.teacher_status}"
    

class TechSupportProfile(TimeStamp, BaseProfile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    custom_user_id = models.UUIDField(null=True)
    school_branch = models.ForeignKey(SchoolBranch, on_delete=models.SET_NULL, null=True, blank=True)
    current_address = models.CharField(max_length=200, null=True, blank=True)
    permanent_address = models.CharField(max_length=200, null=True, blank=True)
    relationship = models.CharField(max_length=15, choices=RELATIONSHIPS, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    salary = models.CharField(max_length=10, default=DEFAULT_SALARY, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="tech_support_profiles", limit_choices_to={'role__in': ALLOWED_MODIFICATION_ROLES})

    def __str__(self):
        return f"Tech Support: {self.user}"


class PrevillagedUserProfile(TimeStamp, BaseProfile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    custom_user_id = models.UUIDField(null=True)
    school_branch = models.ForeignKey(SchoolBranch, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    relationship = models.CharField(max_length=15, choices=RELATIONSHIPS, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="previllaged_profiles", limit_choices_to={'role__in': ALLOWED_MODIFICATION_ROLES}
                                )

    def __str__(self):
        return f"Previllaged User: {self.user}"
    

class Subject(TimeStamp):
    name = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_subjects", limit_choices_to={'role__in': ALLOWED_MODIFICATION_ROLES})

    class Meta:
        verbose_name_plural = "Subjects"

    def __str__(self):
        return f"Subject: {self.name}"
    

class Course(TimeStamp):
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_courses", limit_choices_to={'role__in': ALLOWED_MODIFICATION_ROLES})

    def __str__(self):
        return f"Course: {self.name}"
    

class Topic(TimeStamp):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="topics")
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_topics", limit_choices_to={'role__in': ALLOWED_MODIFICATION_ROLES})

    class Meta:
        ordering = ["name", "created_on"]
        verbose_name_plural = "Topics"

    def __str__(self):
        return f"{self.name[:30]} - {self.subject.name}"
    
    # @property
    # def getTopicName


class ClassName(TimeStamp):
    name = models.CharField(max_length=20, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_class_names", limit_choices_to={'role__in': ALLOWED_MODIFICATION_ROLES})

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Class Names"

    def __str__(self):
        return f"Class Name:{self.name}"


class ClassSection(TimeStamp):
    name = models.CharField(max_length=50, choices=SECTIONS, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_class_sections", limit_choices_to={'role__in': ALLOWED_MODIFICATION_ROLES})

    class Meta:
        verbose_name_plural = "Class Sections"

    def __str__(self):
        return f"{self.name}"


class Class(TimeStamp):
    name = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    section = models.ForeignKey(ClassSection, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_class", limit_choices_to={'role__in': ALLOWED_MODIFICATION_ROLES})

    def __str__(self):
        return f"Class {self.name.name} - {self.section.name}"
    
    class Meta:
        verbose_name_plural = "Classes" 
        ordering = ("name",)
    
    @property
    def getClassName(self):
        return f"{self.name.name} - {self.section.name}"


def classTimeTablePath(instance, filename):
    return f"classTimeTable/{instance.classes}_{instance.section}_{instance.title}/{filename}"


class ClassTimeTable(TimeStamp):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    classes = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    section = models.ForeignKey(ClassSection, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=classTimeTablePath, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Class Time Table" 


    def __str__(self):
        return f"{self.session}-{self.classes}-{self.section}"
    

class ContactUs(TimeStamp):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField(max_length=500)

    class Meta:
        verbose_name_plural = "Contact Us" 

    def __str__(self):
        return f"{self.email} - {self.name} - {self.created_on}"
