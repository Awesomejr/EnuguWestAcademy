from django import forms
from news.models import News, Events
from base.models import Session

from utilities.customStyle.customCSS import INPUT_STYLE, SELECT_STYLE
from utilities.customFuncs import getCurrentSession


class NewsCreationsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "__all__"
        # fields = ["title", "image", "description", "author", "date"]

    title = forms.CharField(label="Title:", required=True, min_length=5, 
                                    widget=forms.TextInput(
                                        attrs={
                                            "class": INPUT_STYLE,
                                            "placeholder": "News title...",
                                        }
                                    ))
    image = forms.ImageField(label="Image",
                                widget=forms.FileInput(attrs={
                                    "placeholder": "Choose File",
                                    "style": "width: 50%",
                                    "id": "postImageInput",
                                    "onchange": "previewImage()",
                                }))
    description = forms.CharField(label="Description:", required=True, min_length=5, 
                                    widget=forms.Textarea(
                                        attrs={
                                            "class": INPUT_STYLE,
                                            "placeholder": "News description...",  
                                            "rows": 5,
                                        }
                                    ))
    author = forms.CharField(label="Author:", required=True, min_length=5, 
                                    widget=forms.TextInput(
                                        attrs={
                                            "class": INPUT_STYLE,
                                            "placeholder": "News author...",  
                                        }
                                    ))
    
    date = forms.DateTimeField(label="Date:", required=True,
                                    widget=forms.DateTimeInput(
                                        attrs={
                                            'type': 'datetime-local',
                                            "class": INPUT_STYLE + "w-full",
                                            },
                                        format='%Y-%m-%dT%H:%M',  # Specify the datetime format
                                    ))


class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = "__all__"

    image = forms.ImageField(label="Image",
                                widget=forms.FileInput(attrs={
                                    "placeholder": "Choose File",
                                    "style": "width: 50%",
                                    "class": INPUT_STYLE,
                                    "id": "postImageInput",
                                    "onchange": "previewImage()",
                                }))

    session = forms.ModelChoiceField(queryset=Session.objects.all(), label="Session", required=True,
                                    initial=getCurrentSession(Session),
                                    widget=forms.Select(
                                        attrs={
                                            "id": "session",
                                            "class": INPUT_STYLE
                                        }
                                    ))

    title = forms.CharField(label="Title:", required=True, min_length=5, 
                                    widget=forms.TextInput(
                                        attrs={
                                            "class": INPUT_STYLE,
                                            "placeholder": "Event title...",
                                        }
                                    ))
    image = forms.ImageField(label="Image",
                                widget=forms.FileInput(attrs={
                                    "placeholder": "Choose File",
                                    "style": "width: 50%",
                                    "id": "postImageInput",
                                    "onchange": "previewImage()",
                                }))
    description = forms.CharField(label="Description:", required=True, min_length=5, 
                                    widget=forms.Textarea(
                                        attrs={
                                            "class": INPUT_STYLE,
                                            "placeholder": "Event description...",
                                            "rows": 5,
                                        }
                                    ))
    date = forms.DateTimeField(label="Date:", required=True,
                                    widget=forms.DateTimeInput(
                                        attrs={
                                            'type': 'date',
                                            "class": INPUT_STYLE,
                                            "placeholder": "Event date...",
                                            },
                                        format='%Y-%m-%dT%H:%M',  # Specify the datetime format
                                    ))
    start_time = forms.TimeField(label="Start Time:", required=True,
                                    widget=forms.TimeInput(
                                        attrs={
                                            'type': 'time',
                                            "class": INPUT_STYLE,
                                            },
                                        format='T%H:%M',  # Specify the datetime format
                                    ))
    close_time = forms.TimeField(label="Close Time:", required=True,
                                    widget=forms.TimeInput(
                                        attrs={
                                            'type': 'time',
                                            "class": INPUT_STYLE,
                                            },
                                        format='T%H:%M',  # Specify the datetime format
                                    ))
    location = forms.CharField(label="Location:", required=True, min_length=5, 
                                    widget=forms.TextInput(
                                        attrs={
                                            "class": INPUT_STYLE,
                                            "placeholder": "Event location...",
                                        }
                                    ))
    host = forms.CharField(label="Host:", required=True, min_length=5, 
                                    widget=forms.TextInput(
                                        attrs={
                                            "class": INPUT_STYLE,
                                            "placeholder": "Event host...",
                                        }
                                    ))