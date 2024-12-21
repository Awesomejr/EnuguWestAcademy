from utilities import customFuncs
from utilities.customVars import *

from base.models import (Subject, Course, ClassName, ClassSection, SchoolBranch)
from blog.models import Category as BlogCategory
from gallery.models import EventCategory
from library.models import Category as LibrayCategory


customFuncs.initialModelData(Model=Subject, Data=SUBJECTS, model_name="Subject")
customFuncs.initialModelData(Model=Course, Data=COURSES, model_name="Course")
# customFuncs.initialModelData(Model=ClassName, Data=ALL_CLASSES, model_name="ClassName")
customFuncs.initialModelData(Model=ClassSection, Data=SECTIONS, model_name="ClassSection")
customFuncs.initialModelData(Model=SchoolBranch, Data=SCHOOL_BRANCHES, model_name="School Branches")

customFuncs.initialModelData(Model=BlogCategory, Data=EXPLORE_CATEGORIES, model_name="Blog Category")

customFuncs.initialModelData(Model=EventCategory, Data=GALLERY_CATEGORIES, model_name="Gallery Category")

customFuncs.initialModelData(Model=LibrayCategory, Data=E_BOOK_CATEGORIES, model_name="Library Category")
