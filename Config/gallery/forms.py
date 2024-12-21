from django import forms

from .models import EventCategory, Event, EventImage
from utilities.customStyle.customCSS import INPUT_STYLE, SELECT_STYLE



class CreateGalleryCategoryForm(forms.ModelForm):
    class Meta:
        model = EventCategory
        fields = ["name"]

    name = forms.CharField(label="Category", required=True, min_length=3, max_length=100, strip=True,
                            widget=forms.TextInput(
                                attrs={
                                    "id": "name",
                                    "class": INPUT_STYLE,
                                    "placeholder": "Category..."
                                }
                            )
                        )
    
    def clean_name(self, *args, **kwargs):
        name = str(self.cleaned_data.get("name")).capitalize().strip()
        if not name.isalpha():
            raise forms.ValidationError("Name Cannot Contain Numbers or Special Characters")
        return name
    

class CreateGalleryEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ["id", "created_by"]
    
    category_qs = EventCategory.objects.all()

    category = forms.ModelChoiceField(queryset=category_qs, label="Category", required=False,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "category",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    title = forms.CharField(label="Title", required=True, 
                                widget=forms.TextInput(
                                    attrs={
                                        "placeholder": "Title of event...",
                                        "name": "title",
                                        "class": INPUT_STYLE
                                    }
                                )
                            )
    date = forms.DateField(label="Date of Event", required=True, 
                                    widget=forms.DateInput(
                                        attrs={
                                            "id": "date",
                                            "class": INPUT_STYLE,
                                            "list": "date-list",
                                            "type": "date"
                                        }
                                    )
                                )


class AddGalleryImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = "__all__"
        exclude = ["id", "created_by"]
    
    category_qs = EventCategory.objects.all()
    event_qs = Event.objects.all()

    category = forms.ModelChoiceField(queryset=category_qs, label="Category", required=False,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "category",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    event = forms.ModelChoiceField(queryset=event_qs, label="Event", required=False,
                                    widget=forms.Select(
                                        attrs={
                                            "id": "event",
                                            "class": INPUT_STYLE
                                        }
                                    ))
    image = forms.ImageField(label=f"Select Image:", required=False,
                            help_text="Image should be JPG/JPEG format.",
                            widget=forms.FileInput(
                                attrs={
                                    "placeholder": "Choose File",
                                    "style": "width: 100%",
                                    "id": "postImageInput",
                                    "onchange": "previewImage()",
                                }
                            ))
    description = forms.CharField(label="Description", required=True, 
                                help_text="Short description of the image.",
                                widget=forms.Textarea(
                                    attrs={
                                        "placeholder": "Image Description...",
                                        "name": "description",
                                        "rows": 5,
                                        "class": INPUT_STYLE
                                    }
                                )
                            )

class GallerySearchForm(forms.Form):
    category = forms.CharField(label="Search", required=True, 
                                widget=forms.TextInput(
                                    attrs={
                                        "placeholder": "Search Category...",
                                        "type": "search", 
                                        "name": "category",
                                        "id": "event_category", 
                                        "list": "category-list", 
                                        "autocomplete": "off",
                                        "class": INPUT_STYLE
                                    }
                                )
                            )