import logging

from django.db import models
from django.core.exceptions import ValidationError

from base.models import Subject, TimeStamp, ClassName
from utilities import customFuncs, customVars


logger = logging.getLogger(__name__)

class Category(TimeStamp):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

# Create your models here.
def eBookPath(instance, filename):
    return f"library/e-books/{instance.title}_{instance.author}/{filename}"


def eBookThumbnailPath(instance, filename):
    return f"library/e-bookThumbnails/{instance.title}_{instance.author}/{filename}"


class Book(TimeStamp):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assigned_class = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    file = models.FileField(upload_to=eBookPath, max_length=300)
    thumbnail = models.ImageField(upload_to=eBookThumbnailPath, blank=True, null=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.title}"
    

    def clean(self):
        if self.file and not self.file.name.endswith(".pdf"):
            raise ValidationError("Only PDF files are allowed.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
