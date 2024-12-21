import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Blog
from utilities.customFuncs import resizeImage


logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Blog)
def createBlogPostThumbnail(sender, instance, **kwargs):
    if instance:
        try:
            logger.info(f"Creating thumbnail for blog post '{instance.title}' image...")
            resized_image = resizeImage(image=instance.cover_image, width=600, height=300)
            instance.cover_image_thumbnail = resized_image
            logger.info("Thumbnail created")
        except Exception as e:
            logger.error(f"{e}")
