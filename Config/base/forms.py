from django import forms
from django.db.models import Q
from django.utils import timezone

from django.contrib.auth.forms import UserCreationForm
from .models import (CustomUser, ParentProfile, StudentProfile, TeacherProfile,
                    Class, PrevillagedUserProfile, Session, Subject, ClassName, ClassSection,
                    Topic, SchoolBranch, Course
                    )
from attendance.models import StudentAttendance, TeacherAttendance

from utilities.customVars import *
from utilities.customStyle.customCSS import INPUT_STYLE, SELECT_STYLE


class ManagementActionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        list_of_actions = kwargs.pop("list_of_actions")
        super().__init__(*args, **kwargs)

        self.fields["action"] = forms.CharField(label="", required=True, 
                                widget=forms.Select(
                                    choices=list_of_actions,
                                    attrs={
                                        "id": "action",
                                        "name": "action",
                                        "class": INPUT_STYLE,
                                        "placeholder": "Select action",
                                    }
                            )
                        )


class LoginForm(forms.Form):
    input_style = """
                    bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white
                """

    username = forms.CharField(label="Your Username", max_length=200, required=True, strip=True,
                                widget=forms.TextInput(
                                    attrs={
                                        "placeholder": "username",
                                        "class": input_style,
                                        "name": "username",
                                        "type": "text",
                                        "id": "username",
                                    }
                                ))
    password = forms.CharField(label="Your Password", max_length=100, required=True, strip=True,
                                widget=forms.PasswordInput(
                                    attrs={
                                        "placeholder": "••••••••",
                                        "class": input_style,
                                        "autocomplete": "off",
                                        "id": "password",
                                        "type": "password",
                                        "name": "password",
                                    }
                                ))


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label='Current Password', required=True, strip=True, max_length=100, min_length=6,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Current Password...",
                                            "class": INPUT_STYLE,
                                            "id": "current-password",
                                        }
                                    ))
    new_password1 = forms.CharField(label='New Password', required=True, strip=True, max_length=100, min_length=6,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "New Password...",
                                            "class": INPUT_STYLE,
                                            "id": "new-password1",
                                        }
                                    ))
    new_password2 = forms.CharField(label='Re-Enter Password', required=True, strip=True, max_length=100, min_length=6,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Re-Enter Password...",
                                            "class": INPUT_STYLE,
                                            "id": "new-password2",
                                        }
                                    ))


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
                    "avatar", "first_name", "last_name", "middle_name", "username", "email", "role"
                ]
    
    avatar = forms.ImageField(label=f"Select avatar:", required=False,
                            help_text="Image size should not excced 400px.",
                            widget=forms.FileInput(
                                attrs={
                                    "placeholder": "Choose File",
                                    "style": "width: 100%",
                                    "id": "postImageInput",
                                    "onchange": "previewImage()",
                                }
                            ))
    first_name = forms.CharField(label='First Name', required=False, strip=True, max_length=50, min_length=3,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "John...",
                                            "class": INPUT_STYLE,
                                            "id": "first-name",
                                            
                                        }
                                    ))
    last_name = forms.CharField(label='Last Name', required=False, strip=True, max_length=50, min_length=3,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Doe...",
                                            "class": INPUT_STYLE,
                                            "id": "last_name",
                                            
                                        }
                                    ))
    middle_name = forms.CharField(label='Middle Name', required=False, strip=True, max_length=20, min_length=3,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Snow..",
                                            "class": INPUT_STYLE,
                                            "id": "middle-name",
                                            
                                        }
                                    ))
    username = forms.CharField(label='Username', required=False, strip=True, max_length=100, min_length=3, disabled=True,
                                help_text="Auto generated",
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Snow..",
                                            "class": INPUT_STYLE,
                                            "id": "username",
                                            
                                        }
                                    ))
    email = forms.CharField(label='Email', required=False, strip=True, max_length=100, min_length=3, disabled=True,
                                help_text="Auto generated",
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Snow..",
                                            "class": INPUT_STYLE,
                                            "id": "middle-name",
                                            "type": "email",
                                        }
                                    ))
    role = forms.CharField(label="Role", required=False, initial="guest", 
                            widget=forms.Select(
                                choices=ROLE_CHOICES_2,
                                attrs={
                                    "id": "role",
                                    "class": INPUT_STYLE
                                }
                            )
                        )


class UpdateUserForm2(forms.Form):
    DISABLE_STATUS = "False"
    
    avatar = forms.ImageField(label=f"Select avatar:", required=False,
                            help_text="Image size should not excced 400px.",
                            widget=forms.FileInput(
                                attrs={
                                    "placeholder": "Choose File",
                                    "style": "width: 100%",
                                    "id": "postImageInput",
                                    "onchange": "previewImage()",
                                }
                            ))
    first_name = forms.CharField(label='First Name', required=False, strip=True, max_length=50, min_length=3,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "John...",
                                            "class": INPUT_STYLE,
                                            "id": "first-name",
                                            "disabled": DISABLE_STATUS,
                                        }
                                    ))
    last_name = forms.CharField(label='Last Name', required=False, strip=True, max_length=50, min_length=3,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Doe...",
                                            "class": INPUT_STYLE,
                                            "id": "last_name",
                                            "disabled": DISABLE_STATUS,
                                        }
                                    ))
    middle_name = forms.CharField(label='Middle Name', required=False, strip=True, max_length=20, min_length=3,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Snow..",
                                            "class": INPUT_STYLE,
                                            "id": "middle-name",
                                            "disabled": DISABLE_STATUS,
                                        }
                                    ))
    username = forms.CharField(label='Username', required=False, strip=True, max_length=100, min_length=3,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Snow..",
                                            "class": INPUT_STYLE,
                                            "id": "username",
                                            "disabled": DISABLE_STATUS,
                                        }
                                    ))
    email = forms.CharField(label='Email', required=False, strip=True, max_length=100, min_length=3,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Snow..",
                                            "class": INPUT_STYLE,
                                            "id": "middle-name",
                                            "type": "email",
                                        }
                                    ))


class UpdateStudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = "__all__"
        exclude = ["id", "user", "custom_user_id"]
    
    school_branch = forms.ModelChoiceField(queryset=SchoolBranch.objects.select_related("manager").all(),
                                    label="Cluster", required=False
                                    )
    classes = forms.ModelChoiceField(queryset=Class.objects.select_related("name", "section", "created_by").all(),
                                    label="Class", required=False
                                    )
    course = forms.ModelChoiceField(
                        queryset=Course.objects.select_related("created_by").prefetch_related("subjects").all(),
                        label="Course", required=False
                    )
    
    registration_number = forms.CharField(label="Registration Number", required=True, disabled=True,
                                            help_text="Auto generated",
                                            widget=forms.TextInput(
                                                attrs={
                                                    "class": INPUT_STYLE,
                                                    "id": "registration-number",
                                                }
                                            )
                                        )
    student_status = forms.CharField(label="Student Status", required=False, help_text=REQUIRED_FIELD,
                                    widget=forms.Select(
                                        choices=STUDENT_STATUS,
                                        attrs={
                                            "id": "student-status",
                                            "class": INPUT_STYLE,
                                        }
                                    ))
    gender = forms.CharField(label="Gender", required=False, help_text=REQUIRED_FIELD,
                                    widget=forms.Select(
                                        choices=GENDER_CHOICES,
                                        attrs={
                                            "id": "gender",
                                            "class": INPUT_STYLE,
                                        }
                                    ))
    date_of_birth = forms.DateField(label="Date of Birth", required=False, help_text=REQUIRED_FIELD,
                                    widget=forms.SelectDateWidget(
                                        years=range(1980, 2030)
                                    ))
    
    nationality = forms.CharField(label="Nationality", required=False, help_text=REQUIRED_FIELD,
                                    widget=forms.Select(
                                        choices=COUNTRIES,
                                        attrs={
                                            "id": "nationality",
                                            "class": INPUT_STYLE,
                                        }
                                    ))
    state = forms.CharField(label="State of Origin", required=True, help_text=REQUIRED_FIELD,
                            widget=forms.Select(
                                choices=STATES,
                                attrs={
                                    "id": "state",
                                    "class": INPUT_STYLE,
                                }
                            ))
    local_government_area = forms.CharField(label="Local Government Area", required=True,
                                            help_text=REQUIRED_FIELD,
                                            widget=forms.TextInput(
                                                attrs={
                                                    "id": "local-government-area",
                                                    "placeholder": "Local Government Area",
                                                    "class": INPUT_STYLE,
                                                }
                                            ))
    town = forms.CharField(label="Town", required=True, help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "town",
                                        "class": INPUT_STYLE,
                                        "placeholder": "Home Town..."
                                    }
                                ))
    religion = forms.CharField(label="Religion", required=False, help_text=REQUIRED_FIELD,
                                widget=forms.Select(
                                    choices=RELIGION_CHOICES,
                                    attrs={
                                        "id": "religion",
                                        "class": INPUT_STYLE,
                                    }
                                ))
    current_address = forms.CharField(label="Current Address", required=True, strip=True,
                                        widget=forms.TextInput(
                                            attrs={
                                                "id": "current-address",
                                                "class": INPUT_STYLE,
                                                "placeholder": "Current Adresss..."
                                            }
                                        )
                                    )
    permanent_address = forms.CharField(label="Permanent Address", required=True, strip=True,
                                        widget=forms.TextInput(
                                            attrs={
                                                "id": "permanent-address",
                                                "class": INPUT_STYLE,
                                                "placeholder": "Permanent Adresss..."
                                            }
                                        )
                                    )
    phone_number = forms.CharField(label='Telephone', required=True, strip=True, max_length=15, min_length=4,
                                    help_text="+234 817826633",
                                    widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Telephone...",
                                            "class": INPUT_STYLE,
                                            "id": "telephone",
                                        }
                                    ))
    previous_school_date = forms.DateField(label="Previous School Date", required=False,
                                    widget=forms.SelectDateWidget(
                                        years=range(1980, 2030)
                                    ))
    reason_for_leaving = forms.CharField(label="Reason For Leaving", max_length=500, required=False,
                                        widget=forms.Textarea(
                                            attrs={
                                                "rows": 4,
                                                "placeholder": "Type your reasons...",
                                                "class": INPUT_STYLE,
                                            }
                                        ))
    disability_description = forms.CharField(label="Disability Description", required=False,
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "disability-description",
                                        "class": INPUT_STYLE,
                                    }
                                ))
    any_disability = forms.CharField(label="Any Disability?", required=False,
                                widget=forms.Select(
                                    choices=YES_NO_LIST,
                                    attrs={
                                        "id": "any-disability",
                                        "class": INPUT_STYLE,
                                    }
                                ))


class UpdateTeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = "__all__"
        exclude = ["id", "custom_user_id", "user", "bio"]

    teacher_status = forms.CharField(label="Teacher Status", required=False, help_text=REQUIRED_FIELD,
                                    widget=forms.Select(
                                        choices=TEACHER_STATUS_LIST,
                                        attrs={
                                            "id": "teacher-status",
                                            "class": INPUT_STYLE,
                                        }
                                    ))
    gender = forms.CharField(label="Gender", required=False, help_text=REQUIRED_FIELD,
                                    widget=forms.Select(
                                        choices=GENDER_CHOICES,
                                        attrs={
                                            "id": "gender",
                                            "class": INPUT_STYLE,
                                        }
                                    ))
    date_of_birth = forms.DateField(label="Date of Birth", required=False, help_text=REQUIRED_FIELD,
                                    widget=forms.SelectDateWidget(
                                        years=range(1980, 2030)
                                    ))
    
    nationality = forms.CharField(label="Nationality", required=False, help_text=REQUIRED_FIELD,
                                    widget=forms.Select(
                                        choices=COUNTRIES,
                                        attrs={
                                            "id": "nationality",
                                            "class": INPUT_STYLE,
                                        }
                                    ))
    state = forms.CharField(label="State of Origin", required=False, help_text=REQUIRED_FIELD,
                            widget=forms.Select(
                                choices=STATES,
                                attrs={
                                    "id": "state",
                                    "class": INPUT_STYLE,
                                }
                            ))
    local_government_area = forms.CharField(label="Local Government Area", required=False,
                                            help_text=REQUIRED_FIELD,
                                            widget=forms.Select(
                                                choices=LOCAL_GOVERNMENT_AREAS,
                                                attrs={
                                                    "id": "local-government-area",
                                                    "class": INPUT_STYLE,
                                                }
                                            ))
    town = forms.CharField(label="Town", required=False, help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "town",
                                        "class": INPUT_STYLE,
                                        "placeholder": "Home Town..."
                                    }
                                ))
    religion = forms.CharField(label="Religion", required=False, help_text=REQUIRED_FIELD,
                                widget=forms.Select(
                                    choices=RELIGION_CHOICES,
                                    attrs={
                                        "id": "religion",
                                        "class": INPUT_STYLE,
                                    }
                                ))


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
                    "avatar", "first_name", "last_name", "middle_name",
                    "password1", "password2"
                ]
        
    avatar = forms.ImageField(label=f"Select avatar:", required=False,
                            help_text="Image size should not excced 400px.",
                            widget=forms.FileInput(
                                attrs={
                                    "placeholder": "Choose File",
                                    "style": "width: 50%",
                                    "id": "postImageInput",
                                    "onchange": "previewImage()",
                                }
                            ))
    first_name = forms.CharField(label='First Name', required=True, strip=True, max_length=20, min_length=3,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "John...",
                                            "class": INPUT_STYLE,
                                            "id": "first-name",
                                        }
                                    ))
    last_name = forms.CharField(label='Last Name', required=True, strip=True, max_length=20, min_length=3,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Doe...",
                                            "class": INPUT_STYLE,
                                            "id": "last_name",
                                        }
                                    ))
    middle_name = forms.CharField(label='Middle Name', required=True, strip=True, max_length=20, min_length=3,
                                help_text=REQUIRED_FIELD,
                                widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Snow..",
                                            "class": INPUT_STYLE,
                                            "id": "middle-name",
                                        }
                                    ))
    password_hint = "Minimum of 6 character is required"
    password1 = forms.CharField(label="Password", required=True, min_length=6, help_text=password_hint, 
                                initial=DEFAULT_PASSWORD,
                                widget=forms.PasswordInput(
                                    attrs={
                                        "class": INPUT_STYLE,
                                        "placeholder": "Password",
                                        "value": DEFAULT_PASSWORD,
                                    }
                                ))
    password2 = forms.CharField(label="Password Confirmation", required=True, min_length=6, help_text=password_hint, 
                                initial=DEFAULT_PASSWORD,
                                widget=forms.PasswordInput(
                                    attrs={
                                        "class": INPUT_STYLE,
                                        "placeholder": "Password Confirmation",
                                        "value": DEFAULT_PASSWORD,
                                    }
                            ))

    def clean_first_name(self, *args, **kwargs):
        first_name = str(self.cleaned_data.get("first_name")).capitalize().strip()
        if not first_name.isalpha():
            raise forms.ValidationError("First Name Cannot Contain Numbers or Special Characters")
        return first_name
    
    def clean_last_name(self, *args, **kwargs):
        last_name = str(self.cleaned_data.get("last_name")).capitalize().strip()
        if not last_name.isalpha():
            raise forms.ValidationError("Last Name Cannot Contain Numbers or Special Characters")
        return last_name

    def clean_middle_name(self, *args, **kwargs):
        middle_name = str(self.cleaned_data.get("middle_name")).capitalize().strip()
        if not middle_name.isalpha():
            raise forms.ValidationError("Middle Name Cannot Contain Numbers or Special Characters")
        return middle_name
    

class ParentProfileForm(forms.ModelForm):
    class Meta:
        model = ParentProfile
        fields = "__all__"
        exclude = ["user", "id", "custom_user_id", "bio", "gender", "date_of_birth"]
    
    school_branch = forms.ModelChoiceField(queryset=SchoolBranch.objects.select_related("manager").all(),
                                    label="Cluster", required=True, help_text="Should be the same with the student cluster."
                                    )

    nationality = forms.CharField(label="Nationality", required=True, initial="Nigeria", help_text=REQUIRED_FIELD,
                                    widget=forms.Select(
                                        choices=COUNTRIES,
                                        attrs={
                                            "id": "nationality",
                                            "class": INPUT_STYLE,
                                        }
                                    ))
    state = forms.CharField(label="State of Origin", required=True, initial="Enugu", help_text=REQUIRED_FIELD,
                            widget=forms.Select(
                                choices=STATES,
                                attrs={
                                    "id": "state",
                                    "class": INPUT_STYLE,
                                }
                            ))
    local_government_area = forms.CharField(label="Local Government Area", required=True, initial="Udi",
                                            help_text=REQUIRED_FIELD,
                                            widget=forms.Select(
                                                choices=LOCAL_GOVERNMENT_AREAS,
                                                attrs={
                                                    "id": "local-government-area",
                                                    "class": INPUT_STYLE,
                                                }
                                            ))
    town = forms.CharField(label="Town", required=True, help_text=REQUIRED_FIELD, initial="Enugwu-Ngwo",
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "town",
                                        "class": INPUT_STYLE,
                                        "placeholder": "Home Town..."
                                    }
                                ))
    religion = forms.CharField(label="Religion", required=True, help_text=REQUIRED_FIELD, initial="Christian",
                                widget=forms.Select(
                                    choices=RELIGION_CHOICES,
                                    attrs={
                                        "id": "religion",
                                        "class": INPUT_STYLE,
                                    }
                                ))
    identification_type = forms.CharField(label="Identification Type", required=False,
                                widget=forms.Select(
                                    choices=IDENTIFICATION_TYPES,
                                    attrs={
                                        "id": "identification_type",
                                        "class": INPUT_STYLE,
                                    }
                                ))
    identification_number = forms.CharField(label='Identification Number', required=False, strip=True, 
                                            max_length=15, min_length=4,
                                            help_text="Your identification type serial digits.",
                                            widget=forms.TextInput(
                                                attrs={
                                                    "placeholder": "789...361",
                                                    "class": INPUT_STYLE,
                                                    "id": "identification-number",
                                                }
                                            ))
    phone_number = forms.CharField(label='Telephone', required=True, strip=True, max_length=15, min_length=4,
                                    help_text="+234 817826633",
                                    widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Telephone...",
                                            "class": INPUT_STYLE,
                                            "id": "telephone",
                                        }
                                    ))
    secondary_phone_number = forms.CharField(label='Seconday Telephone', required=False, strip=True, max_length=15,
                                            min_length=4, help_text="+234 817826633",
                                            widget=forms.TextInput(
                                                attrs={
                                                    "placeholder": "Secondadry Telephone...",
                                                    "class": INPUT_STYLE,
                                                    "id": "secondary-telephone",
                                                }
                                            ))
    father_occupation = forms.CharField(label="Father Occupation", required=False,
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "father-occupation",
                                        "class": INPUT_STYLE,
                                        "placeholder": "Father Occupation...",
                                    }
                                ))
    mother_occupation = forms.CharField(label="Mother Occupation", required=False,
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "mother-occupation",
                                        "class": INPUT_STYLE,
                                        "placeholder": "Mother Occupation...",
                                    }
                                ))
    father_work_address = forms.CharField(label="Father Work Address", required=False,
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "father-work-address",
                                        "class": INPUT_STYLE,
                                        "placeholder": "Father Work Address...",
                                    }
                                ))
    mother_work_address = forms.CharField(label="Mother Work Address", required=False,
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "mother-work-address",
                                        "class": INPUT_STYLE,
                                        "placeholder": "Mother Work Address...",
                                    }
                                ))


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = "__all__"
        exclude = ["user", "id", "custom_user_id", "bio", "parent"]

    
    school_branch = forms.ModelChoiceField(queryset=SchoolBranch.objects.select_related("manager").all(),
                                    label="Cluster", required=True
                                    )
    classes = forms.ModelChoiceField(queryset=Class.objects.select_related("name", "section", "created_by").all(),
                                    label="Class", required=True
                                    )
    course = forms.ModelChoiceField(
                        queryset=Course.objects.select_related("created_by").prefetch_related("subjects").all(),
                        label="Course", required=True
                    )
    student_status = forms.CharField(label="Student Status", required=True, help_text=REQUIRED_FIELD, initial="Full-time",
                                    widget=forms.Select(
                                        choices=STUDENT_STATUS,
                                        attrs={
                                            "id": "student-status",
                                            "class": INPUT_STYLE,
                                        }
                                    ))
    gender = forms.CharField(label="Gender", required=True, help_text=REQUIRED_FIELD, initial="Male",
                                    widget=forms.Select(
                                        choices=GENDER_CHOICES,
                                        attrs={
                                            "id": "gender",
                                            "class": INPUT_STYLE,
                                        }
                                    ))
    date_of_birth = forms.DateField(label="Date of Birth", required=True, help_text=REQUIRED_FIELD,
                                    widget=forms.SelectDateWidget(
                                        years=range(1980, 2030)
                                    ))
    phone_number = forms.CharField(label='Telephone', required=True, strip=True, max_length=15, min_length=4,
                                    help_text="+234 817826633",
                                    widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Telephone...",
                                            "class": INPUT_STYLE,
                                            "id": "telephone",
                                        }
                                    ))
    nationality = forms.CharField(label="Nationality", required=True, initial="Nigeria", help_text=REQUIRED_FIELD,
                                    widget=forms.Select(
                                        choices=COUNTRIES,
                                        attrs={
                                            "id": "nationality",
                                            "class": SELECT_STYLE,
                                        }
                                    ))
    state = forms.CharField(label="State of Origin", required=True, initial="Enugu", help_text=REQUIRED_FIELD,
                            widget=forms.Select(
                                choices=STATES,
                                attrs={
                                    "id": "state",
                                    "class": SELECT_STYLE,
                                }
                            ))
    local_government_area = forms.CharField(label="Local Government Area", required=True, initial="Udi",
                                            help_text=REQUIRED_FIELD,
                                            widget=forms.TextInput(
                                                attrs={
                                                    "id": "local-government-area",
                                                    "placeholder": "Local Government Area...",
                                                    "class": SELECT_STYLE,
                                                }
                                            ))
    town = forms.CharField(label="Town", required=True, help_text=REQUIRED_FIELD, initial="Enugwu-Ngwo",
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "town",
                                        "class": INPUT_STYLE,
                                        "placeholder": "Home Town..."
                                    }
                                ))
    religion = forms.CharField(label="Religion", required=True, help_text=REQUIRED_FIELD, initial="Christian",
                                widget=forms.Select(
                                    choices=RELIGION_CHOICES,
                                    attrs={
                                        "id": "religion",
                                        "class": SELECT_STYLE,
                                    }
                                ))
    current_address = forms.CharField(label="Current Address", required=True, strip=True,
                                        widget=forms.TextInput(
                                            attrs={
                                                "id": "current-address",
                                                "class": INPUT_STYLE,
                                                "placeholder": "Current Adresss..."
                                            }
                                        )
                                    )
    permanent_address = forms.CharField(label="Permanent Address", required=True, strip=True,
                                        widget=forms.TextInput(
                                            attrs={
                                                "id": "permanent-address",
                                                "class": INPUT_STYLE,
                                                "placeholder": "Permanent Adresss..."
                                            }
                                        )
                                    )
    previous_school_date = forms.DateField(label="Previous School Date", required=True,
                                    widget=forms.SelectDateWidget(
                                        years=range(1980, 2030)
                                    ))
    reason_for_leaving = forms.CharField(label="Reason For Leaving", max_length=500, required=False,
                                        widget=forms.Textarea(
                                            attrs={
                                                "rows": 4,
                                                "placeholder": "Type your reasons..."
                                            }
                                        ))
    any_disability = forms.CharField(label="Any Disability?", required=False, initial="No",
                                widget=forms.Select(
                                    choices=YES_NO_LIST,
                                    attrs={
                                        "id": "any-disability",
                                        "class": SELECT_STYLE,
                                    }
                                ))
    

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = "__all__"
        exclude = ["id", "custom_user_id", "bio", "user"]

    class_qs = Class.objects.select_related("name", "section").all()

    assigned_class = forms.ModelMultipleChoiceField(queryset=class_qs, label="Assigned Class", required=True,
                                        help_text="Hold 'Ctrl key' to select multiple options.",
                                        widget=forms.SelectMultiple(
                                            attrs={
                                                "id": "assigned-class",
                                            }
                                        )
                                    )
    teacher_subject = forms.ModelChoiceField(queryset=Subject.objects.select_related("created_by").all(),
                                            label="Teacher Subject", required=True
                                            )
    gender = forms.CharField(label="Gender", required=True, help_text=REQUIRED_FIELD, initial="Male",
                                    widget=forms.Select(
                                        choices=GENDER_CHOICES,
                                        attrs={
                                            "id": "gender",
                                            "class": SELECT_STYLE,
                                        }
                                    ))
    date_of_birth = forms.DateField(label="Date of Birth", required=True, help_text=REQUIRED_FIELD,
                                    widget=forms.SelectDateWidget(
                                        years=range(1980, 2030)
                                    ))
    
    nationality = forms.CharField(label="Nationality", required=True, initial="Nigeria", help_text=REQUIRED_FIELD,
                                    widget=forms.Select(
                                        choices=COUNTRIES,
                                        attrs={
                                            "id": "nationality",
                                            "class": SELECT_STYLE,
                                        }
                                    ))
    state = forms.CharField(label="State of Origin", required=True, initial="Enugu", help_text=REQUIRED_FIELD,
                            widget=forms.Select(
                                choices=STATES,
                                attrs={
                                    "id": "state",
                                    "class": SELECT_STYLE,
                                }
                            ))
    local_government_area = forms.CharField(label="Local Government Area", required=True, initial="Udi",
                                            help_text=REQUIRED_FIELD,
                                            widget=forms.Select(
                                                choices=LOCAL_GOVERNMENT_AREAS,
                                                attrs={
                                                    "id": "local-government-area",
                                                    "class": SELECT_STYLE,
                                                }
                                            ))
    town = forms.CharField(label="Town", required=True, help_text=REQUIRED_FIELD, initial="Enugwu-Ngwo",
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "town",
                                        "class": INPUT_STYLE,
                                        "placeholder": "Home Town..."
                                    }
                                ))
    religion = forms.CharField(label="Religion", required=True, help_text=REQUIRED_FIELD, initial="Christian",
                                widget=forms.Select(
                                    choices=RELIGION_CHOICES,
                                    attrs={
                                        "id": "religion",
                                        "class": INPUT_STYLE,
                                    }
                                ))
    teacher_status = forms.CharField(label="Teacher Status", required=True, help_text=REQUIRED_FIELD, initial="Full-time",
                                widget=forms.Select(
                                    choices=TEACHER_STATUS_LIST,
                                    attrs={
                                        "id": "teacher-status",
                                        "class": INPUT_STYLE,
                                    }
                                ))
    experience_description = forms.CharField(label="Experience Description", max_length=500, required=False,
                                        initial="None",
                                        widget=forms.Textarea(
                                            attrs={
                                                "rows": 4,
                                                "placeholder": "Brief us about your experience..."
                                            }
                                        ))
    cv = forms.FileField(label="Upload CV", required=False, 
                        help_text="pdf, jpeg, jpg formats only.",
                        widget=forms.FileInput(
                            attrs={
                                
                            }
                        ))
    current_address = forms.CharField(label="Current Address", required=False, max_length=100,
                                        widget=forms.TextInput(
                                            attrs={
                                                "id": "current_address",
                                                "placeholder": "Current Address...",
                                                "class": INPUT_STYLE,
                                            }
                                        ))
    phone_number = forms.CharField(label="Telephone", required=True, max_length=15,
                                        widget=forms.TextInput(
                                            attrs={
                                                "id": "phone_number",
                                                "placeholder": "Phone Number...",
                                                "class": INPUT_STYLE,
                                            }
                                        ))
    relationship = forms.CharField(label="Relationship", required=True, help_text=REQUIRED_FIELD, initial="Single",
                                widget=forms.Select(
                                    choices=RELATIONSHIPS,
                                    attrs={
                                        "id": "relationship",
                                        "class": INPUT_STYLE,
                                    }
                                ))
    salary = forms.CharField(label="Salary", required=True, initial="20,000", 
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "salary",
                                        "class": INPUT_STYLE,
                                    }
                                ))


class PrevillagedUserProfileForm(forms.ModelForm):
    role = forms.CharField(label="Role", required=True, initial="guest", 
                            widget=forms.Select(
                                choices=ROLE_CHOICES_2,
                                attrs={
                                    "id": "role",
                                    "class": INPUT_STYLE
                                }
                            )
                        )
    class Meta:
        model = PrevillagedUserProfile
        fields = "__all__"
        exclude = ["id", "custom_user_id", "bio", "user"]


    gender = forms.CharField(label="Gender", required=True, initial="Male",
                                    widget=forms.Select(
                                        choices=GENDER_CHOICES,
                                        attrs={
                                            "id": "gender",
                                            "class": INPUT_STYLE,
                                        }
                                    ))
    date_of_birth = forms.DateField(label="Date of Birth", required=True,
                                    widget=forms.SelectDateWidget(
                                        years=range(1980, 2030),
                                    ))
    
    nationality = forms.CharField(label="Nationality", required=True, initial="Nigeria",
                                    widget=forms.Select(
                                        choices=COUNTRIES,
                                        attrs={
                                            "id": "nationality",
                                            "class": INPUT_STYLE,
                                        }
                                    ))
    state = forms.CharField(label="State of Origin", required=True, initial="Enugu",
                            widget=forms.Select(
                                choices=STATES,
                                attrs={
                                    "id": "state",
                                    "class": INPUT_STYLE,
                                }
                            ))
    local_government_area = forms.CharField(label="Local Government Area", required=True, initial="Udi",
                                            widget=forms.Select(
                                                choices=LOCAL_GOVERNMENT_AREAS,
                                                attrs={
                                                    "id": "local-government-area",
                                                    "class": INPUT_STYLE,
                                                }
                                            ))
    town = forms.CharField(label="Town", required=True, initial="Ngwo",
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "town",
                                        "class": INPUT_STYLE,
                                        "placeholder": "Home Town..."
                                    }
                                ))
    religion = forms.CharField(label="Religion", required=True, initial="Christian",
                                widget=forms.Select(
                                    choices=RELIGION_CHOICES,
                                    attrs={
                                        "id": "religion",
                                        "class": INPUT_STYLE,
                                    }
                                ))
    salary = forms.CharField(label="Salary", required=False, initial="20,000", 
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "salary",
                                        "class": INPUT_STYLE,
                                    }
                                ))
    address = forms.CharField(label="Address", required=False, max_length=100,
                                        widget=forms.TextInput(
                                            attrs={
                                                "id": "current_address",
                                                "placeholder": "Address",
                                                "class": INPUT_STYLE,
                                            }
                                        ))
    phone_number = forms.CharField(label="Telephone", required=True, max_length=15,
                                        widget=forms.TextInput(
                                            attrs={
                                                "id": "phone_number",
                                                "placeholder": "Phone Number...",
                                                "class": INPUT_STYLE,
                                            }
                                        ))
    relationship = forms.CharField(label="Relationship", required=True, initial="Single",
                                widget=forms.Select(
                                    choices=RELATIONSHIPS,
                                    attrs={
                                        "id": "relationship",
                                        "class": INPUT_STYLE,
                                    }
                                ))
    

class StudentAttendanceSearchForm(forms.Form):
    school_branch_qs = SchoolBranch.objects.only("name").all()
    assigned_class_qs = Class.objects.select_related("name", "section", "created_by").all().prefetch_related("subjects")

    school_branch = forms.ModelChoiceField(queryset=school_branch_qs, required=True,
                                            initial=school_branch_qs.first(),
                                            widget=forms.Select(
                                                attrs={
                                                "id": "school-branch",
                                                "class": INPUT_STYLE,
                                                "placeholder": "Search branch name...",
                                            }
                                        )
                                    )
    assigned_class = forms.ModelChoiceField(queryset=assigned_class_qs, required=True,
                                            initial=assigned_class_qs.first(),
                                            widget=forms.Select(
                                                attrs={
                                                    "id": "assigned_class",
                                                    "class": INPUT_STYLE,
                                                    "placeholder": "Search class..."
                                                }
                                            )
                                        )
    date = forms.DateField(required=False, initial=timezone.now().date,
                            widget=forms.DateInput(
                                attrs={
                                        "id": "date",
                                        "class": INPUT_STYLE,
                                        "type": "date",
                                        "list": "date-list",
                                        "format": "%Y:%m:%d"
                                    }
                                )        
                            )


class EditStudentAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = "__all__"
        exclude = ["id", "created_by", "student"]
    
    school_branch_qs = SchoolBranch.objects.only("name").all()
    session_qs = Session.objects.all()
    class_name_qs = Class.objects.select_related("name", "section", "created_by").all().prefetch_related("subjects")

    session = forms.ModelChoiceField(queryset=session_qs, required=True,
                                            initial=session_qs.first(),
                                            widget=forms.Select(
                                                attrs={
                                                "id": "session",
                                                "class": INPUT_STYLE,
                                            }
                                        )
                                    )
    school_branch = forms.ModelChoiceField(queryset=school_branch_qs, required=True,
                                            initial=school_branch_qs.first(),
                                            widget=forms.Select(
                                                attrs={
                                                "id": "school-branch",
                                                "class": INPUT_STYLE,
                                            }
                                        )
                                    )
    class_name = forms.ModelChoiceField(queryset=class_name_qs, required=True,
                                            initial=class_name_qs.first(),
                                            widget=forms.Select(
                                                attrs={
                                                    "id": "assigned_class",
                                                    "class": INPUT_STYLE,
                                                }
                                            )
                                        )
    date = forms.DateField(required=False, initial=timezone.now().date,
                            widget=forms.DateInput(
                                attrs={
                                        "id": "date",
                                        "class": INPUT_STYLE,
                                        "type": "date",
                                        "list": "date-list",
                                        "format": "%Y:%m:%d"
                                    }
                                )        
                            )
    status = forms.CharField(label="Attendance Status", required=True,
                                widget=forms.Select(
                                    choices=ATTENDANCE_STATUS,
                                    attrs={
                                        "id": "status",
                                        "class": INPUT_STYLE,
                                    }
                                )
                            )

    reason_for_absence = forms.CharField(label="Reason for Absence", required=False,
                                            widget=forms.Textarea(
                                                attrs={
                                                    "id": "reason-for-absence",
                                                    "class": INPUT_STYLE,
                                                    "rows": 5,
                                                }
                                            )
                                        )

class TeacherAttendanceSearchForm(forms.Form):
    school_branch_qs = SchoolBranch.objects.only("name").all()
    school_branch = forms.ModelChoiceField(queryset=school_branch_qs, required=True,
                                            initial=school_branch_qs.first(),
                                            widget=forms.Select(
                                                attrs={
                                                "id": "school-branch",
                                                "class": INPUT_STYLE,
                                                "placeholder": "Search branch name...",
                                            }
                                        )
                                    )
    

class CreateSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = "__all__"
        exclude = ["id", "created_by"]
    
    name = forms.CharField(label="Name", required=True,
                                    widget=forms.Select(
                                        choices=BATCHES,
                                        attrs={
                                            "id": "session-name",
                                            "class": INPUT_STYLE,
                                            "placeholder": "Session name...",
                                        }
                                    )
                                )
    session = forms.CharField(label="Session", required=True, help_text="Session format: 2023/2024",
                            widget=forms.TextInput(
                                attrs={
                                        "placeholder": "2023/2024",
                                        "class": INPUT_STYLE,
                                        "id": "session",
                                }
                            )
                        )
    start_date = forms.DateField(label="Start Date", required=True, 
                                    widget=forms.DateInput(
                                        attrs={
                                            "id": "start-date",
                                            "class": INPUT_STYLE,
                                            "list": "date-list",
                                            "type": "date"
                                        }
                                    )
                                )
    closing_date = forms.DateField(label="Closing Date", required=True, 
                                    widget=forms.DateInput(
                                        attrs={
                                            "id": "closing-date",
                                            "class": INPUT_STYLE,
                                            "list": "date-list",
                                            "type": "date"
                                        }
                                    )
                                )
    
    
class CreateSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name"]

    name = forms.CharField(label="Subject Name", required=True,
                                    widget=forms.TextInput(
                                        attrs={
                                            "class": INPUT_STYLE,
                                            "id": "subject",
                                            "placeholder": "Subject name...",
                                        }
                                    )
                                )
    
    def clean_name(self, *args, **kwargs):
        name = str(self.cleaned_data.get("name")).capitalize().strip()
        if not name.isalpha():
            raise forms.ValidationError("Name Cannot Contain Numbers or Special Characters")
        return name


class CreateTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = "__all__"
        exclude = ["id", "created_by"]
    
    name = forms.CharField(label="Topic", required=True,
                            widget=forms.TextInput(
                                attrs={
                                        "placeholder": "Topic...",
                                        "class": INPUT_STYLE,
                                }
                            )
                        )
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Subject", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "subject",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    description = forms.CharField(label="Description", required=False, widget=forms.Textarea(
                                                                attrs={
                                                                    "class": INPUT_STYLE,
                                                                    "placeholder": "Topic short description",
                                                                    "rows": 3,
                                                                }
                                                            )
                                                        )


class CreateSchoolBranchForm(forms.ModelForm):
    class Meta:
        model = SchoolBranch
        fields = "__all__"
        exclude = ["id", "created_by"]


    name = forms.CharField(label="Name", required=True,
                                    widget=forms.TextInput(
                                        attrs={
                                            "class": INPUT_STYLE,
                                            "id": "branch-name",
                                            "placeholder": "Branch name...",
                                        }
                                    )
                                )
    
    def clean_name(self, *args, **kwargs):
        name = str(self.cleaned_data.get("name")).capitalize().strip()
        if not name.isalpha():
            raise forms.ValidationError("Name Cannot Contain Numbers or Special Characters")
        return name


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        exclude = ["id", "created_by"]
    
    name = forms.CharField(label="Name", required=True, strip=True,
                            widget=forms.TextInput(
                                attrs={
                                    "id": "name",
                                    "placeholder": "Course Name...",
                                    "class": INPUT_STYLE
                                }
                            )
                        )
    
    # subjects = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Subjects", required=False,
    #                                 widget=forms.SelectMultiple(
    #                                     attrs={
    #                                         "id": "subject",
    #                                         "class": INPUT_STYLE
    #                                     }
    #                                 ))


class CreateClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = "__all__"
        exclude = ["id",]

    subject_qs = Subject.objects.all().order_by("name")

    name = forms.ModelChoiceField(queryset=ClassName.objects.all(), label="Class Name", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "class-name",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    section = forms.ModelChoiceField(queryset=ClassSection.objects.all(), label="Class Section", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "class-section",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    subjects = forms.ModelMultipleChoiceField(queryset=subject_qs, label="Subjects", required=True,
                                        help_text=REQUIRED_FIELD,
                                        widget=forms.CheckboxSelectMultiple(
                                            attrs={
                                                "id": "subjects",
                                            }
                                        )
                                    )


class EditClassForm(forms.ModelForm):
    new_class_name = forms.CharField(label="New Class Name", required=False, 
                            widget=forms.TextInput(
                                attrs={
                                    "id": "new-class-name",
                                    "class": INPUT_STYLE
                                }
                            )    
                        )
    class Meta:
        model = Class
        fields = "__all__"
        exclude = ["id", "name"]

    subject_qs = Subject.objects.all().order_by("name")

    name = forms.ModelChoiceField(queryset=ClassName.objects.all(), label="Class Name", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "class-name",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    section = forms.ModelChoiceField(queryset=ClassSection.objects.all(), label="Class Section", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "class-section",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    subjects = forms.ModelMultipleChoiceField(queryset=subject_qs, label="Subjects", required=True,
                                        help_text=REQUIRED_FIELD,
                                        widget=forms.CheckboxSelectMultiple(
                                            attrs={
                                                "id": "subjects",
                                            }
                                        )
                                    )


