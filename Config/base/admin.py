from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe
from django.urls import reverse
from django.utils.html import format_html

from .models import (CustomUser, Session, TeacherProfile, ParentProfile, StudentProfile, 
                        ClassName, ClassSection, Class, Subject, Topic, Course, ContactUs,
                        SchoolBranch, ClassTimeTable, TechSupportProfile, PrevillagedUserProfile,
                    )



# Register your models here.
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'session',
        'name',
        'start_date',
        'closing_date',
    )
    list_filter = ('created_on', 'updated_on', 'start_date', 'closing_date')
    search_fields = ('name',)


class CustomUserAdmin(UserAdmin):
    list_per_page = 100
    list_display = ("username", "first_name", "last_name", "middle_name", "displayAvatar", "teacher_profile_link",
                    "student_profile_link", "parent_profile_link")
    # ... other admin configuration ...
    search_fields = ("username", "first_name", "last_name")
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        'created_on',
        'updated_on',
        'role',
        'is_suspended',
        'is_deleted',
    )
    # raw_id_fields = ('groups', 'user_permissions')
    date_hierarchy = "created_on"
    actions_on_top = True
    # actions_on_bottom = True

    fieldsets = [
        ("Custom User Logging Information", {
            "classes": ("collapse", ""),
            "fields": ("id", "username", "password",
                        ),
        }),

        ("Basic Information", {
            "classes": ("collapse", "expanded"),
            "fields": ("avatar", "first_name", "last_name", "middle_name", "email", "role", "is_suspended", "is_deleted"),
        }),

        ("Custom User Metadata", {
            "classes": ("collapse", ""),
            "fields": ("is_superuser", "is_staff", "is_active", "groups",
                        "user_permissions", "last_login", "date_joined",),
        }),
    ]

    def teacher_profile_link(self, obj):
        try:
            teacher_profile = TeacherProfile.objects.get(user=obj)
            teacher_url = reverse(
                "admin:%s_%s_change" % (teacher_profile._meta.app_label, teacher_profile._meta.model_name),
                args=[teacher_profile.pk])
            return format_html('<a href="{}">View Teacher Profile</a>', teacher_url)
        except TeacherProfile.DoesNotExist:
            return "N/A"

    teacher_profile_link.short_description = "Teacher Profile"

    def student_profile_link(self, obj):
        try:
            student_profile = StudentProfile.objects.get(user=obj)
            student_url = reverse(
                "admin:%s_%s_change" % (student_profile._meta.app_label, student_profile._meta.model_name),
                args=[student_profile.pk])
            return format_html('<a href="{}">View Student Profile</a>', student_url)
        except StudentProfile.DoesNotExist:
            return "N/A"

    student_profile_link.short_description = "Student Profile"

    def parent_profile_link(self, obj):
        try:
            parent_profile = ParentProfile.objects.get(user=obj)
            parent_url = reverse(
                "admin:%s_%s_change" % (parent_profile._meta.app_label, parent_profile._meta.model_name),
                args=[parent_profile.pk])
            return format_html('<a href="{}">View Parent Profile</a>', parent_url)
        except ParentProfile.DoesNotExist:
            return "N/A"

    parent_profile_link.short_description = "Parent Profile"

    def displayAvatar(self, obj):
        if obj.avatar:
            return mark_safe(
                f'<img src="{obj.avatar.url}" width="50" height="50" alt="N/A" style="border-radius: 50%;"/>')
        else:
            return "N/A"

    displayAvatar.short_description = "Avatar"


# Register the models and their admins
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(SchoolBranch)
class SchoolBranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_on', 'updated_on', 'name', 'manager')
    list_filter = ('created_on', 'updated_on', 'manager')
    search_fields = ('name',)


@admin.register(PrevillagedUserProfile)
class PrevillagedUserProfileAdmin(admin.ModelAdmin):
    ...


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'bio',
        'gender',
        'date_of_birth',
        'nationality',
        'state',
        'local_government_area',
        'town',
        'religion',
        'user',
        'identification_type',
        'identification_number',
        'address',
        'father_occupation',
        'mother_occupation',
        'father_work_address',
        'mother_work_address',
        'phone_number',
        'secondary_phone_number',
    )
    list_filter = ('created_on', 'updated_on', 'date_of_birth', 'user')

    # fieldsets = [
    #     ("Custom User Logging Information", {
    #         "classes": ("collapse", ""),
    #         "fields": ("id", "username", "password",
    #                     ),
    #     }),

    #     ("Basic Information", {
    #         "classes": ("collapse", "expanded"),
    #         "fields": ("avatar", "first_name", "last_name", "middle_name", "email",
    #                    "gender", "date_of_birth", "bio", "nationality", "state", "local_government_area", "town",
    #                    "religion", "is_student", "is_teacher", "is_school_staff", "is_school_admin", "is_tech_support",),
    #     }),

    #     ("Custom User Metadata", {
    #         "classes": ("collapse", ""),
    #         "fields": ("is_superuser", "is_staff", "is_active", "groups",
    #                     "user_permissions", "last_login", "date_joined",),
    #     }),
    # ]


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        # 'created_on',
        # 'updated_on',
        # 'bio',
        "student_status",
        'gender',
        'date_of_birth',
        'nationality',
        'state',
        'local_government_area',
        'town',
        'religion',
        'user',
        'parent',
        'admission_year',
        'registration_number',
        'session',
        'class_number',
        'is_first_child',
        'is_last_child',
        'current_address',
        'permanent_address',
        'course',
        'classes',
        'previous_school',
        'previous_school_date',
        'reason_for_leaving',
        'any_disability',
        'disability_description',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'date_of_birth',
        'user',
        'parent',
        'admission_year',
        'session',
        'is_first_child',
        'is_last_child',
        'school_branch',
        'course',
        'classes',
        'previous_school_date',
    )
    search_fields = ("registration_number",)

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        # 'created_on',
        # 'updated_on',
        # 'bio',
        'gender',
        'teacher_subject',
        'teacher_status',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'date_of_birth',
        'user',
        'assigned_class',
        'teacher_subject',
    )


@admin.register(TechSupportProfile)
class TechSupportProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'bio',
        'gender',
        'date_of_birth',
        'nationality',
        'state',
        'local_government_area',
        'town',
        'religion',
        'user',
        'custom_user_id',
        'current_address',
        'permanent_address',
        'relationship',
        'phone_number',
        'salary',
    )
    list_filter = ('created_on', 'updated_on', 'date_of_birth', 'user')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_on', 'updated_on', 'name')
    list_filter = ('created_on', 'updated_on')
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_on', 'updated_on', 'name')
    list_filter = ('created_on', 'updated_on')
    # raw_id_fields = ('subjects',)
    search_fields = ('name',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'name',
        'subject',
        'description',
    )
    list_filter = ('created_on', 'updated_on', 'subject')
    search_fields = ('name',)


@admin.register(ClassName)
class ClassNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_on', 'updated_on', 'name')
    list_filter = ('created_on', 'updated_on')
    search_fields = ('name',)


@admin.register(ClassSection)
class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_on', 'updated_on', 'name')
    list_filter = ('created_on', 'updated_on')
    search_fields = ('name',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'name',
        'section',
    )
    list_filter = ('created_on', 'updated_on', 'name', 'section',)
    # raw_id_fields = ('subjects',)
    search_fields = ('name',)


@admin.register(ClassTimeTable)
class ClassTimeTableAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'session',
        'teacher',
        'classes',
        'section',
        'title',
        'image',
    )
    list_filter = (
        'created_on',
        'updated_on',
        'session',
        'teacher',
        'classes',
        'section',
    )


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'name',
        'email',
        'message',
    )
    list_filter = ('created_on', 'updated_on')
    search_fields = ('name',)

