from django.db import models
from base.models import CustomUser, Session, TimeStamp

# Create your models here.
def newsPath(instance, filename):
    return f"news/{instance.title}_{instance.author}/{filename}"


class News(TimeStamp):
    title = models.CharField(max_length=100, null=False)
    image = models.ImageField(upload_to=newsPath, blank=True, null=True)
    description = models.TextField(null=False)
    author = models.CharField(max_length=100, null=True)
    date = models.DateTimeField()

    class Meta:
        verbose_name_plural = "News" 
        ordering = ["created_on", "date"]

    def __str__(self):
        return f"{self.title} - {self.author}"
    

def eventPath(instance, filename):
    return f"news/{instance.title}_{instance.date}_{instance.host}/{filename}"


class Events(TimeStamp):
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, null=False)
    image = models.ImageField(upload_to=eventPath, blank=True, null=True)
    description = models.TextField(null=False)
    date = models.DateField()
    start_time = models.TimeField()
    close_time = models.TimeField()
    location = models.CharField(max_length=200)
    host = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Events" 

    def __str__(self):
        return f"{self.title} - {self.host} - {self.date}"