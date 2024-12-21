SITE_NAME = "EWA"

THURSDAY = 3
FRIDAY = 4
SARTUDAY = 5
SUNDAY = 6
MONDAY = 0

# Choose the type of server and type of database to use!
SERVER_TYPE = "development"
DATABASE_TYPE = "mysql"

REQUIRED_FIELD = "This field is required."

DEFAULT_PASSWORD = "@password"
DEFAULT_SALARY = "20,000"
NUMBER_OF_TABLE_ROW = 50
OPTION_LABELS = ['A', 'B', 'C', 'D']

ALLOWED_MODIFICATION_ROLES = ["administrator", "academic_director", "tech_support", 
                            "mini_tech_support", "superuser", "manager", "mini_manager"]

ALPHABETS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
            ]
    

WEST_AFRICA_COUNTRIES = [
    "Benin",
    "Burkina Faso",
    "Cape Verde",
    "Ivory Coast (Cote d'Ivoire)",
    "Gambia",
    "Ghana",
    "Guinea",
    "Guinea-Bissau",
    "Liberia",
    "Mali",
    "Mauritania",
    "Niger",
    "Nigeria",
    "Senegal",
    "Sierra Leone",
    "Togo"
]

NIGERIA_STATES = {
    "Abia": [],
    "Adamawa": [],
    "Akwa Ibom": [],
    "Anambra": [],
    "Bauchi": [],
    "Bayelsa": [],
    "Benue": [],
    "Borno": [],
    "Cross River": [],
    "Delta": [],
    "Ebonyi": [],
    "Edo": [],
    "Ekiti": [],
    "Enugu": [],
    "Gombe": [],
    "Imo": [],
    "Jigawa": [],
    "Kaduna": [],
    "Kano": [],
    "Katsina": [],
    "Kebbi": [],
    "Kogi": [],
    "Kwara": [],
    "Lagos": [],
    "Nassarawa": [],
    "Niger": [],
    "Ogun": [],
    "Ondo": [],
    "Osun": [],
    "Oyo": [],
    "Plateau": [],
    "Rivers": [],
    "Sokoto": [],
    "Taraba": [],
    "Yobe": [],
    "Zamfara": [],
}

LOCAL_GOVERNMENT_AREAS = [
    ("Aninri", "Aninri"),
    ("Awgu", "Awgu"),
    ("Enugu East", "Enugu East"),
    ("Enugu North", "Enugu North"),
    ("Enugu South", "Enugu South"),
    ("Ezeagu", "Ezeagu"),
    ("Igbo Etiti", "Igbo Etiti"),
    ("Igbo Eze North", "Igbo Eze North"),
    ("Igbo Eze South", "Igbo Eze South"),
    ("Isi Uzo", "Isi Uzo"),
    ("Nkanu East", "Nkanu East"),
    ("Nkanu West", "Nkanu West"),
    ("Nsukka", "Nsukka"),
    ("Oji River", "Oji River"),
    ("Udenu", "Udenu"),
    ("Udi", "Udi"),
    ("Uzo Uwani", "Uzo Uwani"),
]

SCHOOL_TERM = [
    ("First-Term", "First-Term"),
    ("Second-Term", "Second-Term"),
    ("Third-Term", "Third-Term"),
]

YES_NO_LIST = [
    ("No", "No"),
    ("Yes", "Yes"),
]

GENDER_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female"),
]

COUNTRIES = [
    ("Benin", "Benin"),
    ("Burkina Faso", "Burkina Faso"),
    ("Cape Verde", "Cape Verde"),
    ("Ivory Coast (Cote d'Ivoire)", "Ivory Coast (Cote d'Ivoire)"),
    ("Gambia", "Gambia"),
    ("Ghana", "Ghana"),
    ("Guinea", "Guinea"),
    ("Guinea-Bissau", "Guinea-Bissau"),
    ("Liberia", "Liberia"),
    ("Mali", "Mali"),
    ("Mauritania", "Mauritania"),
    ("Niger", "Niger"),
    ("Nigeria", "Nigeria"),
    ("Senegal", "Senegal"),
    ("Sierra Leone", "Sierra Leone"),
    ("Togo", "Togo")
]

STATES = [
    ("Enugu", "Enugu"),
    ("Anambra", "Anambra"),
    ("Imo", "Imo"),
    ("Abia", "Abia"),
    ("Ebonyi", "Ebonyi"),
]

TOWNS = [
    ("Ngwo", "Ngwo"),
    ("9th mile", "9th mile"),
]

SCHOOL_BRANCHES = [
    ("Ngwo", "Ngwo"),
    ("Abor", "Abor"),
    ("Udi", "Udi"),
    ("Oji-River", "Oji-River"),
    ("Nsukka", "Nsukka"),
    # ("", ""),
]


SCHOOL_BRANCHES = [
    ("Mpu-Center(ANNINRI)", "Mpu-Center(ANNINRI)"),
    ("Abor", "Abor"),
    ("Udi", "Udi"),
    ("Oji-River", "Oji-River"),
    ("Nsukka", "Nsukka"),
    # ("", ""),
]




RELIGION_CHOICES = [
    ("Christian", "Christian"),
    ("Muslim", "Muslim"),
    ("Judaism", "Judaism"),
    ("Others", "Others"),
]


SUBJECTS = (
    # ("", ""),
    ("English Language", "English Language"),
    ("Mathematics", "Mathematics"),

    ("Physics", "Physics"),
    ("Biology", "Biology"),
    ("Chemistry", "Chemistry"),

    ("Civic Education", "Civic Education"),
    ("Home Economics", "Home Economics"),
    ("Social Studies", "Social Studies"),
    ("Government", "Government"),
    ("Christian Religious Knowledge", "Christian Religious Knowledge"),

    ("Agricultural Science", "Agricultural Science"),
    ("Igbo Language", "Igbo Language"),
    # ("", ""),
    # ("", ""),
)

QUALIFICATIONS = [
    ("Phd", "Phd"),
    ("Masters", "Masters"),
    ("Bsc", "Bsc"),
    ("Pgd", "Pgd"),
    ("HND", "HND"),
    ("ND", "ND"),
    ("NCE", "NCE"),
    ("WAEC", "WAEC"),
    ("NECO", "NECO"),
    ("NAPTEB", "NAPTEB")
]

DRIVING_QUALIFICATIONS = [
    ("Driver Licence", "Driver Licence"),
    ("FRSC Licence", "FRSC Licence")
]

RELATIONSHIPS = [
    ("Single", "Single"),
    ("Married", "Married"),
    ("Divorced", "Divorced"),
    ("Separated", "Separated"),
    ("Single Parent", "Single Parent")
]

REMARKS = [
    ("Excellent", "Excellent"),
    ("Very Good", "Very Good"),
    ("Good", "Good"),
    ("Fair", "Fair"),
    ("Poor", "Poor"),
]

TEACHER_STATUS_LIST = [
        ("Full-time", "Full-time"),
        ("Part-time", "Part-time"),
    ]


GALLERY_CATEGORIES = [
    ("Graduation", "Graduation"),
    ("Inter-House", "Inter-House"),
    ("Christmas-Party", "Christmas-Party"),
    ("Christmas-Carol", "Christmas-Carol"),
    ("Outings/Excortions", "Outings/Excortions"),
    ("Competitions", "Competitions"),
    ("Birthdays", "Birthdays"),
    ("Toy-day", "Toy-day"),
]


E_BOOK_CATEGORIES = [
    ("Science", "Science"),
    ("Art", "Art"),
    ("Social Science", "Social Science"),
    ("Technology", "Technology"),
    ("Literature", "Literature"),
    ("Novel", "Novel"),
    ("Story Books", "Story Books"),
    ("Biography", "Biography"),
]


EXPLORE_CATEGORIES = [
    ("Science", "Science"),
    ("Art", "Art"),
    ("Social Science", "Social Science"),
    ("Technology", "Technology"),
    ("Literature", "Literature"),
    ("Novel", "Novel"),
    ("Story Books", "Story Books"),
    ("Biography", "Biography"),
]

ROLE_CHOICES = (
        ('administrator', 'Administrator'),
        ('academic_director', 'Academic Director'),
        # ('cluster_manager', 'Cluster Manager'),
        ('data_entry', 'Data Entry'),
        ('manager', 'Manager'),
        ('guest', 'Guest'),
        ('mini_tech_support', 'Mini Tech Support'),
        ('mini_manager', 'Mini Manager'),
        ('parent', 'Parent'),
        ('project_manager', 'Project Manager'),
        # ('school_driver', 'School Driver'),
        ('school_staff', 'School Staff'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('tech_support', 'Tech Support'),
    )

ROLE_CHOICES_2 = (
        # ('administrator', 'Administrator'),
        ('academic_director', 'Academic Director'),
        ('data_entry', 'Data Entry'),
        ('manager', 'Manager'),
        ('guest', 'Guest'),
        ('mini_tech_support', 'Mini Tech Support'),
        ('mini_manager', 'Mini Manager'),
        # ('project_manager', 'Project Manager'),
        # ('school_staff', 'School Staff'),
        ('tech_support', 'Tech Support'),
    )

STUDENT_STATUS = (
    ("Full-time", "Full-time"),
    ("Part-time", "Part-time"),
)

COURSES = (
    ("Engineering", "Engineering"),
    ("Medicine", "Medicine"),
    ("Accounting", "Accounting"),
    ("Administration", "Administration"),
    ("Building-Tech", "Building-Tech"),
    ("Science-Laboratory", "Science-Laboratory"),
    ("Computer-Science", "Computer-Science"),
    # ("", ""),
    # ("", ""),
)

# ALL_CLASSES = (
#     # Science
#     ("Science-Tech", "Science-Tech"), # engineer
#     ("Science-Health", "Science-Health"), # medicine
#     # Social Science
#     ("Humanity", "Humanity"), # law
#     ("Commercial", "Commercial"), # business 

#     ("All", "All"),
#     ("Graduated", "Graduated"),
# )

SECTIONS = (
    ("Section-A", "Section-A"),
    ("Section-B", "Section-B"),
    ("Section-C", "Section-C"),
    ("Default", "Default"),
    ("Graduated", "Graduated"),
)

IDENTIFICATION_TYPES = (
    ("National Identification", "National Identification"),
    ("Personal Voter's Card", "Personal Voter's Card"),
    ("Driver License", "Driver License"),
)

ATTENDANCE_STATUS = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('absent_with_reason', 'Absent with Reason'),
    ]


BATCHES = (
    ("Batch-A", "Batch-A"),
    ("Batch-B", "Batch-B"),
    ("Batch-C", "Batch-C"),
)

EXAM_OPTIONS = (
    ('Option1', 'Option1'), 
    ('Option2', 'Option2'), 
    ('Option3', 'Option3'), 
    ('Option4', 'Option4')
)

QUESTION_DIFFICULTY = (
    ("Easy", "Easy"),
    ("Normal", "Normal"),
    ("Hard", "Hard"),
    ("Advanced", "Advanced"),
)

CTB_TYPE = (
    ("Test", "Test"),
    ("Practice", "Practice"),
)


MANAGEMENT_ACTIONS = (
    (" ", " "),
    ("Delete", "Delete"),
    ("Undelete", "Undelete"),
    ("Reset-Password", "Reset-Password"),
    ("Suspend", "Suspend"),
    ("Unsuspend", "Unsuspend"),
    # ("", ""),
)

ADMIN_MANAGEMENT_ACTIONS = (
    (" ", " "),
    ("Active", "Active"),
    ("Deactive", "Deactive"),
    ("Delete", "Delete"),
    ("Undelete", "Undelete"),
    ("Reset-Password", "Reset-Password"),
    ("Staff", "Staff"),
    ("Suspend", "Suspend"),
    ("Unstaff", "Unstaff"),
    ("Unsuspend", "Unsuspend"),
    # ("", ""),
)

DELETE_MANAGEMENT_ACTION = (
    ("", ""),
    ("Delete", "Delete"),
)



QUESTION_TYPE = (
        ("Past-Question", "Past-Question"),
        ("Teacher-Question", "Teacher-Question"),
        ("Comprehension", "Comprehension"),
    )