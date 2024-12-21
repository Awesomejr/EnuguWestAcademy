import logging

from django.db import models

from base.models import TimeStamp, CustomUser

from utilities import customVars, customFuncs


logger = logging.getLogger(__name__)

# Create your models here.
def eventImageUploadPath(instance, filename):
    return f'gallery/{instance.category.name}_{instance.event.title}/{filename}'


class EventCategory(TimeStamp):
    name = models.CharField(max_length=50)

    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Event Categories" 

    def __str__(self):
        return self.name


class Event(TimeStamp):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    images = models.ManyToManyField('EventImage', related_name='events', blank=True)
    date = models.DateField()

    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Events" 

    def __str__(self):
        return f"{self.category.name}-{self.title}"


class EventImage(TimeStamp):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=eventImageUploadPath)
    description = models.TextField(max_length=200, blank=False)

    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Event Images" 

    def __str__(self):
        return  f"{self.category.name}-{self.description[:50]}"

