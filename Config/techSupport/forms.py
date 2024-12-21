from django import forms
from django.forms import inlineformset_factory
from django.db.models import Q
from django.utils import timezone

from ckeditor.widgets import CKEditorWidget

from base.models import (Session, Subject, Course, CustomUser, Topic, TeacherProfile, 
                        ClassName, SchoolBranch, Class, ClassSection, StudentProfile
                    )
from examination.models import Exam, Question, Option, StudentAnswer, Result, CBTCategory, CBTExam

from utilities import customVars, customFuncs
from utilities.customStyle.customCSS import INPUT_STYLE, SELECT_STYLE


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        exclude = ("exam", "cbt", "exam_practice", "id", "created_by", "number")

    topic_qs = Topic.objects.select_related("subject").none()
    subject_qs = Subject.objects.select_related("created_by").all()

    question_type = forms.CharField(label="Question Type", required=True,
                                        widget=forms.Select(
                                            choices=customVars.QUESTION_TYPE,
                                            attrs={
                                                "id": "question-type",
                                                "class": INPUT_STYLE
                                            }
                                        )
                                    )
    mark = forms.IntegerField(label="Mark", required=False, initial=2,
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "mark",
                                        "type": "number",
                                        "class": INPUT_STYLE
                                    }
                                )
                            )
    subject = forms.ModelChoiceField(queryset=subject_qs, label="Subject", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "subject",
                                            "class": INPUT_STYLE,
                                            "hx-get": "topics-options/",
                                            "hx-target": "#topic",
                                            "hx-indicator": "#loading"
                                        }
                                    ))
    year = forms.IntegerField(label="Year", required=False, initial=timezone.now().year, min_value=1980, max_value=2050,
                                    widget=forms.Select(
                                    choices=customFuncs.generateYears(),
                                    attrs={
                                            "class": INPUT_STYLE,
                                            "id": "year",
                                    }
                                )
                            )
    topic = forms.ModelChoiceField(queryset=topic_qs, label="Topic", required=False,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "topic",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    # number = forms.IntegerField(label="Question Number", required=False, 
    #                                 widget=forms.NumberInput(
    #                                     attrs={
    #                                         "id": "number",
    #                                         "class": INPUT_STYLE
    #                                     }
    #                                 ))
    image = forms.ImageField(label="Select Image", required=False, help_text="jpg/jpeg format only.",
                                    widget=forms.FileInput(
                                        attrs={
                                                    "placeholder": "Choose File",
                                                    "style": "width: 100%",
                                                    "id": "questionImageInput",
                                                    "onchange": "previewImage()",
                                                }
                                            )
                                        )
    
    content = forms.CharField(label="Question Content", required=True, widget=CKEditorWidget(config_name="default",
                                                    attrs={
                                                        "class": INPUT_STYLE,
                                                        "style": "width: 100%;",
                                                        "placeholder": "Question Here...",
                                                        "rows": 10,
                                                        # "id": "q-content"
                                                    }
                                                )
                                            )
    explanation = forms.CharField(label="Explanation", required=False, initial="None",
                                    widget=CKEditorWidget(config_name="default", 
                                                    attrs={
                                                        "class": INPUT_STYLE,
                                                        "placeholder": "Question Explanation Here...",
                                                        "rows": 10,
                                                        # "id": "explanation"
                                                    }
                                                )
                                            )
    level = forms.CharField(label="Level", max_length=30, required=False, initial="Normal",
                            widget=forms.Select(
                                    choices=customVars.QUESTION_DIFFICULTY,
                                    attrs={
                                        "id": "level",
                                        "class": INPUT_STYLE,
                                    }
                                )
                            )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "subject" in self.data:
            subject_id = self.data.get("subject")
            print(f"Subject Id: {subject_id}")
            subject = Subject.objects.get(id=subject_id)
            topics = subject.topics.all()
            self.fields["topic"].queryset = topics


class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        exclude = ("exam", "cbt", "exam_practice", "id", "created_by", "number")

    def __init__(self, *args, **kwargs):
        subject_name = kwargs.pop("subject_name")
        subject_topics =  Topic.objects.filter(subject__name__icontains=subject_name)
        super().__init__(*args, **kwargs)

        self.fields["topic"] = forms.ModelChoiceField(
            queryset=subject_topics, label="Topic", required=False,
            widget=forms.Select(
                attrs={
                    "id": "topic",                                      
                    "class": INPUT_STYLE
                }
            )
        )

    subject_qs = Subject.objects.select_related("created_by").all()

    question_type = forms.CharField(label="Question Type", required=True,
                                        widget=forms.Select(
                                            choices=customVars.QUESTION_TYPE,
                                            attrs={
                                                "id": "question-type",
                                                "class": INPUT_STYLE
                                            }
                                        )
                                    )
    mark = forms.IntegerField(label="Mark", required=False, initial=2,
                                widget=forms.TextInput(
                                    attrs={
                                        "id": "mark",
                                        "type": "number",
                                        "class": INPUT_STYLE
                                    }
                                )
                            )
    subject = forms.ModelChoiceField(queryset=subject_qs, label="Subject", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "subject",
                                            "class": INPUT_STYLE,
                                            # "disabled": True
                                        }
                                    ))
    year = forms.IntegerField(label="Year", required=False, initial=timezone.now().year, min_value=1980, max_value=2050,
                                    widget=forms.Select(
                                    choices=customFuncs.generateYears(),
                                    attrs={
                                            "class": INPUT_STYLE,
                                            "id": "year",
                                    }
                                )
                            )
    # number = forms.IntegerField(label="Question Number", required=False, 
    #                                 widget=forms.NumberInput(
    #                                     attrs={
    #                                         "id": "number",
    #                                         "class": INPUT_STYLE
    #                                     }
    #                                 ))
    image = forms.ImageField(label="Select Image", required=False, help_text="jpg/jpeg format only.",
                                    widget=forms.FileInput(
                                        attrs={
                                                    "placeholder": "Choose File",
                                                    "style": "width: 100%",
                                                    "id": "questionImageInput",
                                                    "onchange": "previewImage()",
                                                }
                                            )
                                        )
    
    content = forms.CharField(label="Question Content", required=True, widget=CKEditorWidget(config_name="default",
                                                    attrs={
                                                        "class": INPUT_STYLE,
                                                        "style": "width: 100%;",
                                                        "placeholder": "Question Here...",
                                                        "rows": 10,
                                                        # "id": "q-content"
                                                    }
                                                )
                                            )
    explanation = forms.CharField(label="Explanation", required=False, widget=CKEditorWidget(config_name="default", 
                                                    attrs={
                                                        "class": INPUT_STYLE,
                                                        "placeholder": "Question Explanation Here...",
                                                        "rows": 10,
                                                        # "id": "explanation"
                                                    }
                                                )
                                            )
    level = forms.CharField(label="Level", max_length=30, required=False,
                            widget=forms.Select(
                                    choices=customVars.QUESTION_DIFFICULTY,
                                    attrs={
                                        "id": "level",
                                        "class": INPUT_STYLE,
                                    }
                                )
                            )


class CreateExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["session", "subject", "year", "total_marks", "duration", "instruction", "published"]
        # exclude = ["created_by", "teacher", "id", "year", "course", "assigned_class", "exam_date"]

    
    session = forms.ModelChoiceField(queryset=Session.objects.all(), label="Session", required=True,
                                    initial=customFuncs.getCurrentSession(Session),
                                    widget=forms.Select(
                                        attrs={
                                            "id": "session",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Subject", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "subject",
                                            "class": INPUT_STYLE
                                        }
                                    ))

    total_marks = forms.CharField(label="Total Mark", required=True, initial=100,
                                    widget=forms.NumberInput(
                                        attrs={
                                            "class": INPUT_STYLE,
                                            "id": "total-mark",
                                        }
                                    )
                                )
    year = forms.IntegerField(label="Year", required=True, min_value=1980, max_value=2050,
                                widget=forms.Select(
                                    choices=customFuncs.generateYears(),
                                    attrs={
                                            "class": INPUT_STYLE,
                                            "id": "year",
                                    }
                                )
                            )
    
    # duration = forms.DurationField(label="Duration", required=True, initial=40,
    #                                 help_text="in mins",
    #                                 widget=forms.NumberInput(
    #                                     attrs={
    #                                         "class": INPUT_STYLE,
    #                                         "id": "duration",
    #                                     }
    #                                 )
    #                             )

    instruction = forms.CharField(label="Instruction", required=True, initial="Answer All Question",
                                    widget=forms.TextInput(
                                        attrs={
                                            "class": INPUT_STYLE,
                                            "id": "instruction",
                                            "list": "instruction-list"
                                        }
                                    )
                                )
    published = forms.BooleanField(label="Publish Exam", required=False, initial=False,
                                    widget=forms.CheckboxInput(
                                        attrs={

                                        }
                                    )
                                    )
    
    # start_time = forms.TimeField(label="Start Time", required=True, 
    #                                 widget=forms.TimeInput(
    #                                     attrs={
    #                                         "id": "start-time",
    #                                         "class": INPUT_STYLE,
    #                                         "list": "start-time-list",
    #                                         "type": "time"
    #                                     }
    #                                 )
    #                             )
    
    # end_time = forms.TimeField(label="End Time", required=True, 
    #                                 widget=forms.TimeInput(
    #                                     attrs={
    #                                         "id": "end-time",
    #                                         "class": INPUT_STYLE,
    #                                         "list": "end-time-list",
    #                                         "type": "time"
    #                                     }
    #                                 )
    #                             )
    
    # exam_date = forms.DateField(label="Exam Date", required=True, 
    #                                 widget=forms.DateInput(
    #                                     attrs={
    #                                         "id": "date",
    #                                         "class": INPUT_STYLE,
    #                                         "list": "date-list",
    #                                         "type": "date"
    #                                     }
    #                                 )
    #                             )
    
    # supervisor = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role="teacher"), 
    #                                 label="Supervisor", required=True,
    #                                 widget=forms.Select(
    #                                     attrs={
    #                                         "id": "supervisor",
    #                                         "class": INPUT_STYLE
    #                                     }
    #                                 )
    #                             )


class CreateExamQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields=[
                "exam", 
                "number",
                "content", 
                "image", 
                "explanation", 
                "topic",
                "level",
            ]
    exam_qs = Exam.objects.select_related("subject", "session", "assigned_class", "course", "created_by").all()
    topic_qs = Topic.objects.select_related("subject").none()

    exam = forms.ModelChoiceField(queryset=exam_qs, label="Exam", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "exam",
                                            "class": INPUT_STYLE,
                                            "hx-get": "topics-options/",
                                            "hx-target": "#topic",
                                            "hx-indicator": "#loading"
                                        }
                                    ))
    topic = forms.ModelChoiceField(queryset=topic_qs, label="Topic", required=False,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "topic",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    number = forms.IntegerField(label="Question Number", required=False, 
                                    widget=forms.NumberInput(
                                        attrs={
                                            "id": "number",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    image = forms.ImageField(label="Select Image", required=False,
                                    widget=forms.FileInput(
                                        attrs={
                                                    "placeholder": "Choose File",
                                                    "style": "width: 100%",
                                                    "id": "questionImageInput",
                                                    "onchange": "previewImage()",
                                                }
                                            )
                                        )
    
    content = forms.CharField(label="Question Content", widget=CKEditorWidget(config_name="default", 
                                                    attrs={
                                                        "class": INPUT_STYLE,
                                                        "style": "width: 100%;",
                                                        "placeholder": "Question Here...",
                                                        "rows": 10,
                                                        # "id": "q-content"
                                                    }
                                                )
                                            )
    explanation = forms.CharField(label="Explanation", widget=CKEditorWidget(config_name="default", 
                                                    attrs={
                                                        "class": INPUT_STYLE,
                                                        "placeholder": "Question Explanation Here...",
                                                        "rows": 10,
                                                        # "id": "explanation"
                                                    }
                                                )
                                            )
    level = forms.CharField(label="Level", max_length=30, required=False,
                            widget=forms.Select(
                                    choices=customVars.QUESTION_DIFFICULTY,
                                    attrs={
                                        "id": "level",
                                        "class": INPUT_STYLE,
                                    }
                                )
                            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "exam" in self.data:
            exam_id = self.data.get("exam")
            print(f"Exam Id: {exam_id}")
            exam = Exam.objects.get(id=exam_id)
            topics = exam.subject.topics.all()
            self.fields["topic"].queryset = topics
        

class EditExamQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields=[
                "exam", 
                "number",
                "content", 
                "image", 
                "explanation", 
                "topic",
                "level",
            ]


    exam_qs = Exam.objects.select_related("subject", "session", "assigned_class", "course", "created_by").all()
    topic_qs = Topic.objects.select_related("subject").all()

    exam = forms.ModelChoiceField(queryset=exam_qs, label="Exam", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "exam",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    topic = forms.ModelChoiceField(queryset=topic_qs, label="Topic", required=False,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "topic",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    number = forms.IntegerField(label="Question Number", required=False, 
                                    widget=forms.NumberInput(
                                        attrs={
                                            "id": "number",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    image = forms.ImageField(label="Select Image", required=False,
                                    widget=forms.FileInput(
                                        attrs={
                                                    "placeholder": "Choose File",
                                                    "style": "width: 100%",
                                                    "id": "questionImageInput",
                                                    "onchange": "previewImage()",
                                                }
                                            )
                                        )
    
    content = forms.CharField(label="Question Content", widget=CKEditorWidget(config_name="default", 
                                                    attrs={
                                                        "class": INPUT_STYLE,
                                                        "style": "width: 100%;",
                                                        "placeholder": "Question Here...",
                                                        "rows": 10,
                                                        # "id": "q-content"
                                                    }
                                                )
                                            )
    explanation = forms.CharField(label="Explanation", widget=CKEditorWidget(config_name="default", 
                                                    attrs={
                                                        "class": INPUT_STYLE,
                                                        "placeholder": "Question Explanation Here...",
                                                        "rows": 10,
                                                        # "id": "explanation"
                                                    }
                                                )
                                            )
    level = forms.CharField(label="Level", max_length=30, required=False,
                            widget=forms.Select(
                                    choices=customVars.QUESTION_DIFFICULTY,
                                    attrs={
                                        "id": "level",
                                        "class": INPUT_STYLE,
                                    }
                                )
                            )


class CreateOptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["content", "image", "is_correct"]

        # Customize widgets, labels, and other field options here
        widgets = {
            'content': CKEditorWidget(config_name="default", 
                                    attrs={
                                            'class': INPUT_STYLE, 
                                            'placeholder': 'Option content here..',
                                            "style": "width: 100%;",
                                            "rows": 5,
                                            # "required": "true",
                                        }
                                    ),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full', "id": "optionImageInput"}),
            'is_correct': forms.CheckboxInput(attrs={'class': "", "type":"checkbox", "id": "is-correct"}),
        }
        labels = {
            'content': 'Option Content',
            'image': 'Upload Image (optional)',
            'is_correct': 'Is Correct Answer?',
        }


# Inline formset for managing multiple options for a single question
OptionFormSet = inlineformset_factory(
    Question,
    Option,
    form=CreateOptionForm,
    fields=["content", "image", "is_correct"],
    extra=4, # Number of options per question
    can_delete=False # Ensure exactly 4 options are present
)



class CreateCBTCategoryForm(forms.ModelForm):
    class Meta:
        model = CBTCategory
        fields = "__all__"
        exclude = ["created_by", "id"]
    
    sesion_qs = Session.objects.all()
    class_qs = Class.objects.select_related("name", "section", "created_by").prefetch_related("subjects").all()
    school_branch_qs = SchoolBranch.objects.select_related("manager", "created_by").all()
    supervisor_qs = CustomUser.objects.filter(
        Q(role="teacher") | Q(role="tech_support")
    )

    session = forms.ModelChoiceField(queryset=sesion_qs, label="Session", required=True,
                                    initial=customFuncs.getCurrentSession(Session),
                                    help_text=customVars.REQUIRED_FIELD,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "session",
                                            "class": INPUT_STYLE
                                        }
                                    )
                                )
    school_branch = forms.ModelMultipleChoiceField(queryset=school_branch_qs, label="Cluster", required=True,
                                        help_text="Hold 'Ctrl key' to select multiple options.",
                                        widget=forms.SelectMultiple(
                                            attrs={
                                                "id": "school-branch",
                                                "class": INPUT_STYLE,
                                                # "required": True,
                                            }
                                        )
                                    )
    assigned_class = forms.ModelChoiceField(queryset=class_qs, label="Assigned Class", required=True,
                                    help_text=customVars.REQUIRED_FIELD,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "assigned_class",
                                            "class": INPUT_STYLE
                                        }
                                    )
                                )
    description = forms.CharField(label="Description", required=True, initial="CBT Exam",
                                    help_text=customVars.REQUIRED_FIELD,
                                    widget=forms.Textarea(
                                        attrs={
                                            "placeholder": "description",
                                            "id": "description",
                                            "class": INPUT_STYLE,
                                            "rows": 5
                                        }
                                    )        
                                )
    number_of_subject = forms.IntegerField(label="Number of Subjects", min_value=3, max_value=4, required=True,
                                            initial=4,
                                            widget=forms.NumberInput(
                                                attrs={
                                                    "id": "number-of-subjects",
                                                    "class": INPUT_STYLE
                                                }
                                            )
                                        )
    # duration = forms.IntegerField(label="Duration", required=True, initial=120,
    #                                 help_text="in mins",
    #                                 widget=forms.TextInput(
    #                                     attrs={
    #                                         "class": INPUT_STYLE,
    #                                         "id": "duration",
    #                                         "type": "text"
    #                                     }
    #                                 )
    #                             )
    
    start_time = forms.TimeField(label="Start Time", required=True, help_text=customVars.REQUIRED_FIELD,
                                widget=forms.TimeInput(
                                    attrs={
                                        "id": "start-time",
                                        "class": INPUT_STYLE,
                                        "list": "start-time-list",
                                        "type": "time"
                                    }
                                )
                            )
    
    end_time = forms.TimeField(label="End Time", required=True, help_text=customVars.REQUIRED_FIELD,
                                widget=forms.TimeInput(
                                    attrs={
                                        "id": "end-time",
                                        "class": INPUT_STYLE,
                                        "list": "end-time-list",
                                        "type": "time"
                                    }
                                )
                            )
    
    exam_date = forms.DateField(label="Exam Date", required=True, help_text=customVars.REQUIRED_FIELD,
                                widget=forms.DateInput(
                                    attrs={
                                        "id": "date",
                                        "class": INPUT_STYLE,
                                        "list": "date-list",
                                        "type": "date"
                                    }
                                )
                            )
    supervisor = forms.ModelChoiceField(queryset=supervisor_qs, label="Supervisor", required=True,
                                    help_text=customVars.REQUIRED_FIELD,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "supervisor",
                                            "class": INPUT_STYLE
                                        }
                                    )
                                )


class CreateCBTExamForm(forms.Form):
    cbt_category_qs = CBTCategory.objects.defer("session").select_related(
        "assigned_class", "assigned_class__name", "assigned_class__section").all()
    sesion_qs = Session.objects.all()
    supervisor_qs = CustomUser.objects.filter(
        Q(role="teacher") | Q(role="manager") | Q(role="mini_tech_support")
    )
    subjects = [(subject.name, subject.name) for subject in Subject.objects.only("name").all()]


    session = forms.ModelChoiceField(queryset=sesion_qs, label="Session", required=True,
                                    initial=customFuncs.getCurrentSession(Session),
                                    help_text=customVars.REQUIRED_FIELD,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "session",
                                            "class": INPUT_STYLE
                                        }
                                    )
                                )
    cbt_category = forms.ModelChoiceField(queryset=cbt_category_qs, label="CBT Category", required=True,
                                    help_text=customVars.REQUIRED_FIELD,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "cbt-category",
                                            "class": INPUT_STYLE
                                        }
                                    )
                                )
    
    subjects = forms.MultipleChoiceField(choices=subjects, label="Subjects", required=True,
                                        help_text=customVars.REQUIRED_FIELD,
                                        widget=forms.CheckboxSelectMultiple(
                                            attrs={
                                                "id": "subjects",
                                            }
                                        )
                                    )
    
    # duration = forms.IntegerField(label="Duration", required=True, initial=120,
    #                                 help_text="in mins",
    #                                 widget=forms.NumberInput(
    #                                     attrs={
    #                                         "class": INPUT_STYLE,
    #                                         "id": "duration",
    #                                     }
    #                                 )
    #                             )
    
    # start_time = forms.TimeField(label="Start Time", required=True, 
    #                             widget=forms.TimeInput(
    #                                 attrs={
    #                                     "id": "start-time",
    #                                     "class": INPUT_STYLE,
    #                                     "list": "start-time-list",
    #                                     "type": "time"
    #                                 }
    #                             )
    #                         )
    
    # end_time = forms.TimeField(label="End Time", required=True, 
    #                             widget=forms.TimeInput(
    #                                 attrs={
    #                                     "id": "end-time",
    #                                     "class": INPUT_STYLE,
    #                                     "list": "end-time-list",
    #                                     "type": "time"
    #                                 }
    #                             )
    #                         )
    
    # exam_date = forms.DateField(label="Exam Date", required=True, 
    #                             widget=forms.DateInput(
    #                                 attrs={
    #                                     "id": "date",
    #                                     "class": INPUT_STYLE,
    #                                     "list": "date-list",
    #                                     "type": "date"
    #                                 }
    #                             )
    #                         )
    
    # supervisor = forms.ModelChoiceField(queryset=supervisor_qs, label="Supervisor", required=True,
    #                                 help_text=customVars.REQUIRED_FIELD,
    #                                 widget=forms.Select(
    #                                     attrs={
    #                                         "id": "supervisor",
    #                                         "class": INPUT_STYLE
    #                                     }
    #                                 )
    #                             )


class CreateCBTQuestionsForm(forms.Form):
    cbt_category_qs = CBTCategory.objects.select_related("assigned_class", "session").all()
    cbt_exams_qs = CBTExam.objects.none()
    # subject_names = [exam.subject.name for exam in cbt_exams_qs]
    topics_qs = Topic.objects.none()
    # topics_qs = Topic.objects.filter(subject__name__in=subject_names)

    cbt_category = forms.ModelChoiceField(queryset=cbt_category_qs, label="CBT Category.", required=True,
                                    initial=cbt_category_qs.last(),
                                    widget=forms.Select(
                                        attrs={
                                            "id": "cbt_category",
                                            "class": INPUT_STYLE,
                                            "hx-get": "cbt-exams-options/",
                                            "hx-target": "#cbt-exam",
                                            "hx-indicator": "#loading"
                                        }
                                    ))
    cbt_exam = forms.ModelChoiceField(queryset=cbt_exams_qs, label="CBT Exams", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "cbt-exam",
                                            "class": INPUT_STYLE,
                                        }
                                    ))
    exam_topic = forms.ModelChoiceField(queryset=topics_qs, label="Topics", required=False,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "exam_topic",
                                            "class": INPUT_STYLE,
                                        }
                                    ))