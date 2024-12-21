import datetime
import random
import logging
from pprint import pprint

from django.utils import timezone
from base.models import CustomUser, ClassName, Subject, Class, Course, SchoolBranch, Topic
from examination.models import Exam, Question, Option

from utilities import customFuncs, customVars
from faker import Faker


logger = logging.getLogger(__name__)
fake = Faker()

def randomDates() -> list:
    dates = []
    start_date = datetime.date(2024, 9, 10)
    end_date = datetime.date(2024, 10, 10)
    
    #Represent the difference between two datetime objects.
    delta = datetime.timedelta(days=1) 

    while start_date <= end_date:
        dates.append(start_date.isoformat())
        start_date += delta
    return dates


def generateParentStudentTestData(UserModel: object, ParentModel: object, 
                                StudentModel: object, current_session: object, 
                                student_course: str, student_class: str,
                                number: int = 20) -> None:

    course = Course.objects.filter(name__icontains=student_course).first()
    student_class = Class.objects.filter(name__name__icontains=student_class).first()
    school_branches = SchoolBranch.objects.all().select_related("manager")

    for index in range(number):
        school_branch = random.choice(school_branches)

        parent_first_name=fake.first_name()
        parent_last_name=fake.last_name()
        parent_middle_name=fake.first_name()
        nationality = []
        states = []
        local_government_areas = []
        religions = []
        identification_types =[]
        customFuncs.deconstructItems(customVars.COUNTRIES, nationality)
        customFuncs.deconstructItems(customVars.STATES, states)
        customFuncs.deconstructItems(customVars.LOCAL_GOVERNMENT_AREAS, local_government_areas)
        customFuncs.deconstructItems(customVars.RELIGION_CHOICES, religions)
        customFuncs.deconstructItems(customVars.IDENTIFICATION_TYPES, identification_types)

        logger.info(f"Creating Parent Account!!! {index}")
        parent = UserModel.objects.create(
            first_name=parent_first_name,
            last_name=parent_last_name,
            middle_name=parent_middle_name,
            role="parent",
            username=customFuncs.generateUsername(first_name=parent_first_name, last_name=parent_last_name),
            email=customFuncs.generateUserEmail(
                first_name=parent_first_name, last_name=parent_last_name, middle_name=parent_middle_name
                )
        )
        parent.set_password(customVars.DEFAULT_PASSWORD)
        parent.save()
        logger.info(f"Done Creating '{parent.getFullName}' Parent Account!!! {index}")

        logger.info(f"Updating Parent Profile!!! {index}")
        parent_profile = ParentModel.objects.get(user=parent)
        parent_profile.school_branch = school_branch
        parent_profile.nationality = random.choice(nationality)
        parent_profile.state = random.choice(states)
        parent_profile.local_government_area = random.choice(local_government_areas)
        parent_profile.town = fake.country()
        parent_profile.religion = random.choice(religions)
        parent_profile.identification_type = random.choice(identification_types)
        parent_profile.identification_number = fake.numerify("###########") 
        parent_profile.father_occupation = fake.word()
        parent_profile.mother_occupation = fake.word()
        parent_profile.father_work_address = fake.address()
        parent_profile.mother_work_address = fake.address()
        parent_profile.phone_number = fake.numerify("070########")
        parent_profile.secondary_phone_number = fake.numerify("081########")
        parent_profile.save()
        logger.info(f"Done Updating '{parent.getFullName}' Parent Profile!!! {index}")

        
        logger.info(f"Updating Student Profile!!! {index}")
        student_profile = StudentModel.objects.get(parent=parent_profile)
        student_profile.gender = random.choice(["Male", "Female"])
        student_profile.nationality = random.choice(nationality)
        student_profile.state = random.choice(states)
        student_profile.local_government_area = random.choice(local_government_areas)
        student_profile.town = fake.country()
        student_profile.religion = random.choice(religions)
        student_profile.phone_number = fake.numerify("091########")
        student_profile.date_of_birth = fake.date_of_birth(minimum_age=16, maximum_age=20)
        student_profile.registration_number = customFuncs.generateStudentRegistrationNumber(
            current_session=current_session, parent_first_name=parent_first_name, parent_last_name=parent_last_name
        )
        student_profile.session = current_session
        student_profile.course = course
        student_profile.classes = student_class
        student_profile.student_status = random.choice(["Full-time", "Part-time"])
        student_profile.school_branch = school_branch
        student_profile.permanent_address = fake.address()
        student_profile.save()
        logger.info(f"Done Updating '{student_profile.user.getFullName}' Student Profile!!! {index}")


        student_first_name=fake.first_name()
        student_last_name=fake.last_name()
        student_middle_name=fake.first_name()

        logger.info(f"Updating Student Account!!! {index}")
        student = student_profile.user
        student.first_name = student_first_name
        student.last_name = parent_last_name
        student.middle_name = student_middle_name
        student.role = "student"
        student.set_password(customVars.DEFAULT_PASSWORD)
        student.username = customFuncs.generateStudentUsername(
                    first_name=student_first_name, last_name=student_last_name
                )
        student.email = customFuncs.generateUserEmail(
                    first_name=student_first_name, last_name=student_last_name, middle_name=student_middle_name
                )
        student.save()
        logger.info(f"Done Updating Student Account!!! {index}")
    logger.info(f"Test Data Generation Complete")

        

def studentClassAttendance(Model: object, students: list, 
                            created_by:object, current_session: object) -> None:
    reason = ""
    week_day = customFuncs.getWeekDay()
    dates = randomDates()
    for date in dates:
        # if week_day == customVars.SARTUDAY or week_day == customVars.SUNDAY:
        for student in students:
            logger.info(f"Starting Attendance For {date}.... \n")
            status = random.choice(["present", "absent", "absent_with_reason"])
            if status == "absent_with_reason":
                reason = fake.paragraph(nb_sentences=2)
            else:
                reason = ""
            student_attendance, created = Model.objects.get_or_create(
                        student=student,
                        class_name=student.classes,
                        school_branch=student.school_branch,
                        session=current_session,
                        date=date,
                        status = status,
                        reason_for_absence=reason,
                        created_by=created_by,
                    )
            student_attendance.save()
            logger.info(f"{student.user.getFullName} Attendance For {date}.")
        logger.info(f"Ending Attendance For {date}!!! \n")
    logger.info("Attendance Created.")



def studentRandomActivities(Model: object, teacher_class: object, class_section:object, teacher:object, current_session: object) -> None:

    dates = randomDates()
    for date in dates:
        logger.info(f"Creating Activities For {date}.... \n")
        new_activity = Model.objects.create(
            session = current_session,
            title = fake.word(),
            activity = fake.paragraph(5),
            classes = teacher_class,
            class_section = class_section,
            submission_date = date,
            teacher = teacher,
            is_complete = False
        )
        new_activity.save()
        logger.info(f"Created Activities For {date}!!! \n")
    logger.info("Activities Created.")



def generateTeacher(UserModel: object, TeacherModel: object, number: int=30) -> None:
    courses = Course.objects.all().prefetch_related("subjects")
    all_subjects = Subject.objects.all()
    all_class = Class.objects.select_related("name", "section", "created_by").all().prefetch_related("subjects")
    school_branches = SchoolBranch.objects.all().select_related("manager")

    for index in range(number):
        first_name=fake.first_name()
        last_name=fake.last_name()
        middle_name=fake.first_name()
        nationality = []
        states = []
        local_government_areas = []
        religions = []
        qualifications =[]
        relationship =[]
        yes_no_list =[]
        customFuncs.deconstructItems(customVars.COUNTRIES, nationality)
        customFuncs.deconstructItems(customVars.STATES, states)
        customFuncs.deconstructItems(customVars.LOCAL_GOVERNMENT_AREAS, local_government_areas)
        customFuncs.deconstructItems(customVars.RELIGION_CHOICES, religions)
        customFuncs.deconstructItems(customVars.QUALIFICATIONS, qualifications)
        customFuncs.deconstructItems(customVars.RELATIONSHIPS, relationship)
        customFuncs.deconstructItems(customVars.YES_NO_LIST, yes_no_list)

        any_experience = random.choice(yes_no_list)
        if any_experience == "Yes":
            experience_description = fake.paragraph(nb_sentences=3)
        else:
            experience_description = "None"
        teacher_subject = random.choice(all_subjects)
        

        logger.info(f"Creating Teacher Account!!! {index}")
        teacher = UserModel.objects.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            role="teacher",
            username=customFuncs.generateUsername(first_name=first_name, last_name=last_name),
            email=customFuncs.generateUserEmail(
                first_name=first_name, last_name=last_name, middle_name=middle_name
                )
        )
        teacher.set_password(customVars.DEFAULT_PASSWORD)
        teacher.save()
        logger.info(f"Done Creating '{teacher.getFullName}' Account!!! {index}")

        logger.info(f"Updating Teacher Profile!!! {index}")
        teacher_profile = TeacherModel.objects.get(user=teacher)
        teacher_profile.nationality = random.choice(nationality)
        teacher_profile.gender = random.choice(["Male", "Female"])
        teacher_profile.date_of_birth = fake.date_of_birth(minimum_age=25, maximum_age=35)
        teacher_profile.state = random.choice(states)
        teacher_profile.local_government_area = random.choice(local_government_areas)
        teacher_profile.town = fake.country()
        teacher_profile.religion = random.choice(religions)
        teacher_profile.any_experience = any_experience
        teacher_profile.experience_description = experience_description
        teacher_profile.school_branch = random.choice(school_branches)
        teacher_profile.qualification = random.choice(qualifications)
        teacher_profile.relationship = fake.numerify("###########") 
        teacher_profile.current_address = fake.address()
        teacher_profile.permanent_address = fake.address()
        teacher_profile.phone_number = fake.numerify("070########")
        teacher_profile.teacher_status = "Full-time"
        teacher_profile.teacher_subject = teacher_subject

        if teacher_subject == "English Language" or teacher_subject == "Mathematics":
            for class_ in all_class:
                teacher_profile.assigned_class.add(class_)
        else:
            teacher_profile.assigned_class.add(random.choice(all_class)) 
        teacher_profile.save()
        logger.info(f"Done Updating '{teacher.getFullName}' Teacher Profile!!! {index}")
    logger.info(f"Test Data Generation Complete")


def generateTopics(TopicModel: object, request: object, number: int = 200) -> None:
    subjects = Subject.objects.only("name").all()

    for index in range(number):
        subject = random.choice(subjects)
        logger.info(f"{index}: Creating Topic For {subject.name}... \n")
        TopicModel.objects.create(
            name = fake.text(random.randint(30, 60)),
            subject = subject,
            description = fake.paragraph(nb_sentences=random.randint(2, 5)),
            created_by = request.user
        )
        
        logger.info(f"{index}: Topic For {subject.name} Has been created. \n")

    logger.info(f"{number} Topics Has Been Created Successfully.")


def generateQuestions(request: object, number_of_questions_per_subject: int=150, 
                        single_subject: bool=False, subject_name=None):
    if single_subject:
        subject = Subject.objects.select_related("created_by").filter(name__icontains=subject_name).first()
        topics = subject.topics.all()
        for index in range(number_of_questions_per_subject):
            question = Question.objects.create(
                question_type=random.choices(["Past-Question", "Teacher-Question"]),
                subject=subject,
                year=random.randint(a=2000, b=2030),
                content=fake.paragraph(nb_sentences=random.randint(2, 5)),
                explanation=fake.paragraph(nb_sentences=random.randint(2, 5)),
                mark=2,
                topic=random.choice(topics),
                level="Normal",
                created_by=request.user,
            )
            logger.info(f"Question {index + 1} created for {subject.name}")
            generateQuestionOption(question, request)
            logger.info(f"Questions created for {subject.name}")
        logger.info(f"Question Created Complete.")
    else:
        subjects = Subject.objects.select_related("created_by").all()

        for subject in subjects:
            topics = subject.topics.all()
            for index in range(number_of_questions_per_subject):
                question = Question.objects.create(
                    question_type=random.choices(["Past-Question", "Teacher-Question"]),
                    subject=subject,
                    year=random.randint(a=2000, b=2030),
                    content=fake.paragraph(nb_sentences=random.randint(2, 5)),
                    explanation=fake.paragraph(nb_sentences=random.randint(2, 5)),
                    mark=2,
                    topic=random.choice(topics),
                    level="Normal",
                    created_by=request.user,
                )
                logger.info(f"Question {index + 1} created for {subject.name}")
                generateQuestionOption(question, request)
            logger.info(f"Questions created for {subject.name}")
        logger.info(f"Question Created Complete.")


def generateExamination(ExamModel: object, request: object, current_session: object, 
                        exam_class: str, exam_date=None, number_per_subject: int =10) -> None:
    # Set default for exam_date if not provided
    exam_date = exam_date or timezone.now().date()
    
    teachers = CustomUser.objects.filter(role="teacher")
    exam_class = ClassName.objects.filter(name__icontains=exam_class).first()
    subjects = Class.objects.filter(name=exam_class).first().subjects.all()
    # courses = Course.objects.prefetch_related("subjects").all()

    for subject_index, subject in enumerate(subjects, start=1):
        logger.info(f"Round {subject_index}: Creating '{number_per_subject}' Exam(s) for {subject.name}...")

        for index in range(number_per_subject):
            # Random exam start and end times (if needed)
            start_time = timezone.now().time()
            end_time = (timezone.now() + datetime.timedelta(hours=2)).time()  # Example: 2-hour duration
            
            try:
                exam = ExamModel.objects.create(
                    session=current_session,
                    # course=random.choice(courses),
                    assigned_class=exam_class,
                    subject=subject,
                    year=str(random.randint(2000, 2024)),
                    duration=datetime.timedelta(hours=2),  # Example: Set duration to 2 hours
                    start_time=start_time,
                    end_time=end_time,
                    exam_date=exam_date,
                    supervisor=random.choice(teachers),
                    created_by=request.user,
                )
                logger.info(f"Exam {index + 1} created: {exam.getExamName}")
            
            except Exception as e:
                logger.error(f"Error creating exam for {subject.name}: {e}")
                continue  # Skip to the next exam in case of an error
    logger.info(f"Examinations Created Successfully!")



def generateExamQuestion(request: object, number_of_question_per_exam: int = 20) -> None:
    exams = Exam.objects.select_related(
        "session", "course", "subject", "teacher", "supervisor", "created_by"
    ).all()

    for exam_index, exam in enumerate(exams, start=1):
        logger.info(
            f"Round {exam_index}: Creating '{number_of_question_per_exam}' Exam Questions for {exam.getExamName}...")
        
        exam_related_topics = exam.subject.topics.all()

        for index in range(number_of_question_per_exam):
            content = " ".join(fake.paragraphs(nb=random.randint(1, 4)))
            explanation = " ".join(fake.paragraphs(nb=random.randint(1, 6)))
            topic = random.choice(exam_related_topics)

            question = Question.objects.create(
                exam=exam,
                number=index + 1,
                content=content,
                explanation=explanation,
                topic=topic,
                created_by=request.user
            )

            logger.info(f"Question {index + 1} created: {question.exam.getExamName}")
            generateQuestionOption(question, request)

        logger.info(f"Done Creating Exam Questions For {exam.getExamName}")

    logger.info(f"Questions Created Successfully!")


def generateQuestionOption(QuestionModel: object, request: object, number_of_options: int = 4) -> None:
    logger.info(f"Creating Options for {QuestionModel.subject.name}")
    
    correct_option_index = random.randint(0, number_of_options - 1)  # One correct option

    for index in range(number_of_options):
        option = Option.objects.create(
            question=QuestionModel,
            content=fake.text(random.randint(10, 30)),
            is_correct=index == correct_option_index,  # Mark one as correct
            created_by=request.user,
        )

        logger.info(f"Option {index + 1} Created for {option.question.subject.name}")
    
    logger.info(f"Done Creating Options for {QuestionModel.subject.name}")




# def createBlogs(Model: object, number_of_blogs: int = 500) -> None:
#     class_list = ClassName.objects.all()
#     authors = CustomUser.objects.filter(is_teacher=True)
#     categories = Category.objects.all()
#     subjects = Subject.objects.all()

#     logger.info(f"Creating blog posts... \n")
#     for i in range(number_of_blogs):
#         Model.objects.create(
#             category = random.choice(categories),
#             assigned_class = random.choice(class_list),
#             subject = random.choice(subjects),
#             author = random.choice(authors),
#             title = fake.text(random.randint(20, 50)),
#             introduction = fake.paragraph(10),
#             content = fake.paragraph(60),
#             published = True
#         )
#         logger.info(f"Done Creating Blog Post {i} \n")
#     logger.info(f"Blog Posts Creation Complete")

