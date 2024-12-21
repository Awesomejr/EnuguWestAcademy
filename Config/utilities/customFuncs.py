import logging
import random
import datetime
from io import BytesIO

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import redirect

from utilities import customVars

logger = logging.getLogger(__name__)


def getWeekDay(increment_by: int= 0) -> int:
    week_day = None
    if increment_by:
        week_day = datetime.datetime.today().weekday() + increment_by
    else:
        week_day = datetime.datetime.today().weekday() #+ 5
    return week_day


def getCurrentSession(Model: object) -> object:
    try:
        current_session = Model.objects.latest("created_on")
        logger.info(f"CURRENT_SESSION: {current_session}")
    except:
        current_session = ""
    return current_session


def getSession(Model: object, current_session: object) -> object:
    session = Model.objects.filter(session__icontains=current_session.session).first().session
    logger.info(f"SESSION: {session}")
    return session


def generateStudentUsername(first_name: str, last_name: str) -> str:
    random_number = random.randint(1_000, 9_999)
    return f"{first_name}{last_name}{random_number}@{customVars.SITE_NAME}.com".lower()


def generateUserEmail(first_name: str, last_name: str, middle_name: str) -> str:
    random_number = random.randint(1_000, 9_999)
    return f"{first_name}{last_name}{middle_name}{random_number}@{customVars.SITE_NAME}.com".lower()


def generateUsername(first_name: str, last_name: str) -> str:
    random_number = random.randint(1_000, 9_999)
    return f"{first_name}{last_name}{random_number}".lower()


def generateStudentRegistrationNumber(current_session: object, parent_first_name: str, parent_last_name: str) -> str:
    random_number = random.randint(1_000, 9_999)
    return f"{customVars.SITE_NAME}/{current_session.session}/{random_number}{ parent_first_name[0].upper()}{ parent_last_name[0].upper()}"


def getUser(Model: object, user_id: str, request: object, errorMessages: object, redirect_link= None) -> object:
    user = None
    try:
        user = Model.objects.get(id=user_id) # Get the user
    except Model.DoesNotExist:
        logger.error(f"User does not exists!!!")
        errorMessages.error(request, f"User does not exists. You are not a user!!!")
        if redirect_link == None:
            pass
        else:
            return redirect(redirect_link)
    return user


def getStudentAccounts(CustomUserModel: object, delete_status: int=0) -> list:
    return CustomUserModel.objects.filter(role="student", is_deleted=delete_status)


def getStudentProfiles(StudentProfileModel: object, session: object, delete_status: int=0) -> list:
    return StudentProfileModel.objects.select_related(
        "user", "classes__name", "classes__section", "school_branch", "session", "course", "parent",
        "parent__user", "school_branch__manager", "school_branch__created_by"
    ).filter(session=session, user__is_deleted=delete_status).all().order_by("-created_on")


def getParentAccounts(CustomUserModel: object, delete_status: int=0) -> list:
    return CustomUserModel.objects.filter(role="parent", is_deleted=delete_status)


def getParentProfiles(ParentProfileModel: object, session: object, delete_status: int=0) -> list:
    return ParentProfileModel.objects.select_related(
        "user", "session",
    ).filter(session=session, user__is_deleted=delete_status).all().order_by("-created_on")


def getTeacherAccounts(CustomUserModel: object, delete_status: int=0) -> list:
    return CustomUserModel.objects.filter(role="teacher", is_deleted=delete_status)


def getTeacherProfiles(TeacherProfileModel: object, delete_status: int=0) -> list:
    return TeacherProfileModel.objects.select_related(
                                            "user", "teacher_subject", "school_branch", "created_by"
                                        ).prefetch_related(
                                            "assigned_class", "assigned_class__name",
                                            "assigned_class__section"
                                        ).filter(
                                            user__is_deleted=delete_status
                                        ).all().order_by("-created_on")

def getPrevillagedUsersProfiles(PrevillagedUsersProfileModel: object, delete_status: int=0) -> list:
    return PrevillagedUsersProfileModel.objects.select_related(
                                            "user", "school_branch", "created_by"
                                        ).filter(
                                            user__is_deleted=delete_status
                                        ).all().order_by("-created_on")

def getManagerProfile(request: object) -> object:
    return request.user.previllageduserprofile

def deconstructItems(items: list, list_: list) -> object:
    for item in items:
        list_.append(item[0])
    list_.sort()


def resizeImage(image, width:int=300, height:int=300, format:str="image/jpeg") -> bytes:
    # Open the image image using Pillow
    image_to_resize = Image.open(image)

    # Resize the image to the desired dimensions (e.g., 150x150 pixels)
    resized_image = image_to_resize.resize((width, height))

    # Save the resized image to a BytesIO object
    output = BytesIO()
    resized_image.save(output, format='JPEG')

    # Create a new SimpleUploadedFile from the BytesIO content
    resized_avatar = SimpleUploadedFile(f"{image.name}", output.getvalue(), content_type=f"{format}")

    return resized_avatar


def displayFormErrors(request: object, form: object, messages: object, logger: object) -> None:
    # Form is not valid, display error messages to the user
    for field, errors in form.errors.items():
        for error in errors:
            logger.error(f"{field.capitalize()}: {error}")
            messages.error(request, f"{field.capitalize()}: {error}")



def shuffleTwoList(item_1: list, item_2: list) -> list:
    zipped_list = list(zip(item_1, item_2))
    random.shuffle(zipped_list)
    return zip(*zipped_list) 


def initialModelData(Model: object, Data: list, model_name: str) -> None:
    queryset = Model.objects.all()
    if queryset:
        logger.info(f"{model_name} Already Added to Database!!!")
    else:
        results = []
        deconstructItems(Data, results)
        results.sort()
        try:
            for result in results:
                Model(name=result).save()
        except Exception as e:
            logger.error(f"{type(e).__name__}: {e}")
            pass


def generateYears(start_year: int=1980, end_year: int =2031) -> list:
    years = []
    for year in range(start_year, end_year):
        years.append((year, year))
    return years


def objectModificationLog(request: object, logger: object, object_name: str) -> None:
    logger.info(
        f"""{request.user.getFullName} - {request.user.username} 
        is attempting CRUD operation for {object_name.capitalize()}...""".capitalize()
    )


def deleteAllRequestsLogs() -> None:
    from request.models import Request
    qs = Request.objects.all()
    qs.delete()