import logging

from django.db import models
from ckeditor.fields import RichTextField

from base.models import TimeStamp, CustomUser, ClassName, Subject

from utilities import customVars, customFuncs


logger = logging.getLogger(__name__)

# Create your models here.
def blogCoverImagePath(instance, filename):
    return f"blogCoverImages/{instance.author}_{instance.title[:20]}/{filename}"

def blogCoverImageThumbnailPath(instance, filename):
    return f"blogCoverThumbnailImages/{instance.author}_{instance.title[:20]}/{filename}"


class Category(TimeStamp):
    name = models.CharField(max_length=200, choices=customVars.EXPLORE_CATEGORIES)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


class Blog(TimeStamp):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    assigned_class = models.ForeignKey(ClassName, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    read_time = models.IntegerField(default=2)
    introduction = RichTextField(null=True, blank=True)
    content = RichTextField()
    cover_image = models.ImageField(upload_to=blogCoverImagePath, blank=True, null=True)
    cover_image_thumbnail=models.ImageField(upload_to=blogCoverImageThumbnailPath, blank=True, null=True)
    published = models.BooleanField(default=False)
    make_public = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(CustomUser, blank=True, related_name="liked_blogs")

    def __str__(self):
        return f"{self.author} - {self.title}"
    
    @property
    def shortDescription(self):
        words = self.content.split()
        if len(words) > 10:
            return " ".join(words[:10]) + "... "
        else:
            return self.content[:10]
    
    @property
    def likesCount(self):
        return self.liked_by.count()


class Comment(TimeStamp):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    liked_by = models.ManyToManyField(CustomUser, blank=True, related_name="liked_comments")

    class Meta:
        ordering = ("-created_on",)

    def __str__(self):
        return f"Comment by {self.author.user.username or self.author.user.email} on {self.post.title}"
    
    @property
    def likesCount(self):
        return self.liked_by.count()
    

class Like(TimeStamp):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("user", "post")
    
    def __str__(self):
        return f"{self.user.username or self.user.email} likes {self.post.title}"
    
