from django.urls import path

from . import views, cbtViews, deleteViews, examinationViews


app_name = "techsupport"

urlpatterns = [
        path("dashboard/", views.dashboard, name="dashboard"),

        path("register-parent/", views.registerParent, name="registerParent"),
        path("register-student/<uuid:parentID>/", views.registerStudent, name="registerStudent"),
        path("register-teacher/", views.registerTeacher, name="registerTeacher"),
        path("register-previllaged-user/", views.registerPrevillagedUser, name="registerPrevillagedUser"),

        path("view-custom-users/", views.viewCustomUsers, name="viewCustomUsers"),

        path("view-students/", views.viewStudents, name="viewStudents"),
        path("edit-student/<uuid:studentId>/", views.editStudent, name="editStudent"),

        path("view-parents/", views.viewParents, name="viewParents"),
        path("view-parent/<uuid:parentId>/", views.viewParent, name="viewParent"),

        path("view-teachers/", views.viewTeachers, name="viewTeachers"),
        path("edit-teacher/<uuid:teacherId>/", views.editTeacher, name="editTeacher"),

        path("view-previllaged-users/", views.viewPrevillagedUsers, name="viewPrevillagedUsers"),
        path("view-previllaged-user/<uuid:userId>/", views.viewPrevillagedUser, name="viewPrevillagedUser"),
        path("edit-previllaged-user/<uuid:userId>/", views.editPrevillagedUser, name="editPrevillagedUser"),
        path("delete-previllaged-user/<uuid:userId>/", deleteViews.deletePrevillagedUser, name="deletePrevillagedUser"),
        
        path("students-attendance/", views.studentsAttendance, name="studentsAttendance"),
        path("preview-students-marked-attendance/", views.previewStudentsMarkedAttendance, name="previewStudentsMarkedAttendance"),
        path("students-attendance-statistics/", views.studentsAttendanceStatistics, name="studentsAttendanceStatistics"),
        path("take-students-attendance/<str:school_branch_id>/<str:class_id>/", 
                views.takeStudentsAttendance, name="takeStudentsAttendance"
                ),
        path("view-student-attendance/<uuid:studentId>/", views.viewStudentAttendance, name="viewStudentAttendance"),
        path("edit-student-attendance/<uuid:attendanceId>/", views.editStudentAttendance, name="editStudentAttendance"),

        path("teacher-attendance/", views.teacherAttendance, name="teacherAttendance"),
        path("view-teacher-attendance/<uuid:teacherId>/", views.viewTeacherAttendance, name="viewTeacherAttendance"),
        path("take-teacher-attendance/<str:school_branch_id>/", 
                views.takeTeacherAttendance, name="takeTeacherAttendance"
                ),

        path("create-session/", views.createSession, name="createSession"),
        path("create-subject/", views.createSubject, name="createSubject"),
        path("create-topic/", views.createTopic, name="createTopic"),
        path("create-school-branch/", views.createSchoolBranch, name="createSchoolBranch"),
        path("create-class/", views.createClass, name="createClass"),
        path("create-course/", views.createCourse, name="createCourse"),

        path("edit-session/<uuid:sessionId>/", views.editSession, name="editSession"),
        path("edit-school-branch/<uuid:schoolBranchId>/", views.editSchoolBranch, name="editSchoolBranch"),
        path("edit-class/<uuid:classId>/", views.editClass, name="editClass"),
        path("edit-topic/<uuid:topicId>/", views.editTopic, name="editTopic"),
        path("edit-subject/<uuid:subjectId>/", views.editSubject, name="editSubject"),

        path("delete-student/<uuid:studentId>/", deleteViews.deleteStudent, name="deleteStudent"),
        path("delete-teacher/<uuid:teacherId>/", deleteViews.deleteTeacher, name="deleteTeacher"),

        path("delete-session/<uuid:sessionId>/", deleteViews.deleteSession, name="deleteSession"),
        path("delete-school-branch/<uuid:schoolBranchId>/", deleteViews.deleteSchoolBranch, name="deleteSchoolBranch"),
        path("delete-topic/<uuid:topicId>/", deleteViews.deleteTopic, name="deleteTopic"),
        path("delete-subject/<uuid:subjectId>/", deleteViews.deleteSubject, name="deleteSubject"),
        path("delete-class/<uuid:classId>/", deleteViews.deleteClass, name="deleteClass"),
        path("delete-course/<uuid:courseId>/", deleteViews.deleteCourse, name="deleteCourse"),

        path("create-question/", views.createQuestion, name="createQuestion"),
        path("create-question/topics-options/", views.topicsOptions, name="topicsOptions"),
        path("edit-question/<uuid:questionId>/", views.editQuestion, name="editQuestion"),
        path("edit-question-options/<uuid:questionId>/", views.editQuestionOptions, name="editQuestionOptions"),
        path("view-question/", views.viewQuestions, name="viewQuestions"),
        path("view-question-with-options/<uuid:questionId>/", views.viewQuestionWIthOptions, name="viewQuestionWIthOptions"),
        path("delete-question/<uuid:questionId>/", deleteViews.deleteQuestion, name="deleteQuestion"),

        path("create-examination/", examinationViews.createExamination, name="createExamination"),
        path("edit-examination/<uuid:examId>/", examinationViews.editExamination, name="editExamination"),
        path("preview-examination/", examinationViews.previewExamination, name="previewExamination"),
        path("print-examination/<uuid:examId>/", examinationViews.printExamination, name="printExamination"),
        path("publish-examination/<uuid:examId>/", examinationViews.publishExamination, name="publishExamination"),
        

        path("create-examination-question/", examinationViews.createExaminationQuestion, name="createExaminationQuestion"),
        path("create-examination-question/topics-options/", examinationViews.topicsOptions, name="topicsOptions"),
        path("preview-examination-question/", examinationViews.previewExaminationQuestion, name="previewExaminationQuestion"),
        path("edit-examination-question/<uuid:questionId>/", examinationViews.editExaminationQuestion, name="editExaminationQuestion"),

        path("delete-examination/<uuid:examId>/", deleteViews.deleteExamination, name="deleteExamination"),
        path("delete-examination-question/<uuid:questionId>/", deleteViews.deleteExaminationQuestion, name="deleteExaminationQuestion"),

        path("create-examination-question-option/<uuid:questionId>/", examinationViews.createExaminationQuestionOption, name="createExaminationQuestionOption"),
        path("preview-examination-question-option/", examinationViews.previewExaminationQuestionOption, name="previewExaminationQuestionOption"),


        path("create-cbt-category/", cbtViews.createCBTCategory, name="createCBTCategory"),
        path("edit-cbt-category/<uuid:cbtCategoryId>/", cbtViews.editCBTCategory, name="editCBTCategory"),
        path("create-cbt-exam/", cbtViews.createCBTExam, name="createCBTExam"),
        path("preview-cbt-category/", cbtViews.previewCBTCategory, name="previewCBTCategory"),
        path("publish-cbt-category/<uuid:cbtCategoryId>/", cbtViews.publishCBTCategory, name="publishCBTCategory"),
        path("create-cbt-question/<uuid:cbtCategoryId>/", cbtViews.createCBTQuestion, name="createCBTQuestion"),
        path("remove-cbt-question/<uuid:cbtCategoryId>/<uuid:cbtExamId>/<uuid:questionId>/", cbtViews.removeCBTQuestion, name="removeCBTQuestion"),
        path("preview-cbt-exam/<uuid:cbtCategoryId>/", cbtViews.previewCBTExamination, name="previewCBTExamination"),
        path("delete-cbt-category/<uuid:cbtCategoryId>/", deleteViews.deleteCBTCategory, name="deleteCBTCategory"),
        path("load-cbt-exam/<uuid:cbtExamId>/", cbtViews.loadCBTExamQuestions, name="loadCBTExamQuestions"),

        path("view-cbt-scores/", cbtViews.viewCBTScores, name="viewCBTScores"),
        path("view-cbt-exams/<uuid:cbtCategoryId>/", cbtViews.viewCBTCategoryExams, name="viewCBTCategoryExams"),
        path("cbt-analysis/<uuid:cbtCategoryId>/", cbtViews.viewCBTAnalysis, name="viewCBTAnalysis"),

        path("preview-cbt-results/", cbtViews.previewCBTResults, name="previewCBTResults"),
        path("publish-cbt-results/<uuid:cbtCategoryId>/", cbtViews.publishCBTResults, name="publishCBTResults"),
        path("delete-cbt-result/<uuid:cbtResultId>/", deleteViews.deleteCBTResult, name="deleteCBTResult"),
]