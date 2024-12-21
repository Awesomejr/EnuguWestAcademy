from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Blog, Category
from base.models import Subject, ClassName
from utilities.customStyle.customCSS import INPUT_STYLE, SELECT_STYLE


class PostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = (
            "cover_image", "category", "subject", "assigned_class", "title", 
            "read_time", "introduction", "content", "published", "make_public",
        )

    category_qs = Category.objects.all()
    subject_qs = Subject.objects.all()
    class_qs = ClassName.objects.all()


    category = forms.ModelChoiceField(queryset=category_qs, label="Category", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "category",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    subject = forms.ModelChoiceField(queryset=subject_qs, label="Subject", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "subject",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    assigned_class = forms.ModelChoiceField(queryset=class_qs, label="Class", required=True,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "assigned-class",
                                            "class": INPUT_STYLE
                                        }
                                    ))

    cover_image = forms.ImageField(label="Cover image", required=True,
                                    widget=forms.FileInput(attrs={
                                        "placeholder": "Choose File",
                                        "style": "width: 50%",
                                        "id": "postImageInput",
                                        "onchange": "previewImage()",
                                    }))
    title = forms.CharField(label="Title", required=True, 
                                    widget=forms.TextInput(
                                        attrs={
                                            "placeholder": "Title...",
                                            "class": INPUT_STYLE,
                                        }
                                    ))
    read_time = forms.IntegerField(label="Read Time", required=True, initial=2, 
                                    widget=forms.TextInput(
                                        attrs={
                                            "type": "number",
                                            "class": INPUT_STYLE,
                                        }
                                    )
                                )
    introduction = forms.CharField(widget=CKEditorWidget(config_name="default", attrs={
                                        "placeholder": "Type your content's introduction here...",
                                        "class": INPUT_STYLE,
                                    }))
    content = forms.CharField(widget=CKEditorWidget(config_name="default", attrs={
                                        "placeholder": "Type main content here...",
                                        "class": INPUT_STYLE,
                                    }))


