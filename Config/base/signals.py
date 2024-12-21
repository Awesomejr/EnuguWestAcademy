import logging

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from .models import (CustomUser, StudentProfile, TeacherProfile, ParentProfile, ContactUs, 
                    Session, PrevillagedUserProfile
                )

from utilities import customFuncs

logger = logging.getLogger(__name__)
CURRENT_SESSION = customFuncs.getCurrentSession(Session)


@receiver(post_save, sender=CustomUser)
def createParentToStudentAccountAndProfile(sender, instance, created, **kwargs) -> None:
    if created:
        logger.info(f"{instance.getFullName} Account Has Been Created.")
        if instance.role == "parent":
            logger.info(f"Attempting To Create Parent Profile...")
            parent_profile = ParentProfile.objects.create(user=instance, custom_user_id=instance.id,
                                                            session=CURRENT_SESSION
                                                        ) 
            logger.info(f"Parent Profile For {instance.getFullName} Has Been Created.")

            logger.info(f"Attempting To Create Student Account For Parent...")
            student = CustomUser.objects.create(last_name=instance.last_name, 
                                                middle_name=instance.middle_name, 
                                                username=customFuncs.generateStudentUsername(
                                                                    first_name=instance.middle_name,
                                                                    last_name=instance.last_name
                                                                ),
                                                role="student"
                                            )
            logger.info(f"Student Account For 'Parent: {instance.getFullName}' Has Been Created.")

            parent_profile = ParentProfile.objects.select_related("user").get(user=instance)

            logger.info(f"Attempting To Create Student Profile...")
            StudentProfile.objects.create(
                    user=student, 
                    custom_user_id=student.id,
                    parent=parent_profile, 
                    session=CURRENT_SESSION,
                    nationality= parent_profile.nationality, 
                    state= parent_profile.state,
                    local_government_area = parent_profile.local_government_area,
                    town=parent_profile.town,
                    religion=parent_profile.religion,
                    permanent_address=parent_profile.address,
                    school_branch=parent_profile.school_branch,
                )
            logger.info(f"Student Profile For 'Parent: {instance.getFullName}' Has Been Created.")
        elif instance.role == "teacher":
            logger.info(f"Attempting To Create Teacher Profile...")
            TeacherProfile.objects.create(user=instance, custom_user_id=instance.id) 
            logger.info(f"Teacher Profile For {instance.getFullName} Has Been Created.")
        elif instance.role == "mini_tech_support" or instance.role == "guest" or instance.role == "manager" or \
                        instance.role == "administrator" or instance.role == "mini_manager" or \
                        instance.role == "academic_director" or instance.role == "data_entry":
            logger.info(f"Attempting To Create Previllaged User Profile...")
            PrevillagedUserProfile.objects.create(user=instance, custom_user_id=instance.id) 
            logger.info(f"Previllaged User Profile For {instance.getFullName} Has Been Created.")
