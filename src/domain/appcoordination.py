from domain.entity import Student, Assignment, Grade
from infrastructure.repositories import StudentRepo, AssignmentRepo, GradeRepo, FileStudentRepo, \
    FileAssignmentRepo, FileGradeRepo, BinaryStudentRepo, BinaryAssignmentRepo, BinaryGradeRepo
from ui.console import UI
from domain.validators import StudentValidator, AssignmentValidator, GradeValidator
from infrastructure.repositories import UndoRedoRepo
from services.service import StudentService, AssignmentService, GradeService, UndoRedoSrv
import configparser


class AppCoord:
    def __init__(self):
        self.__studentRepo = None
        self.__assignmentRepo = None
        self.__gradeRepo = None

    def __init_inmemory(self):
        # for initialising the repository information in case we choose to use the in memory repos
        self.__studentRepo = StudentRepo()
        self.__assignmentRepo = AssignmentRepo()
        self.__gradeRepo = GradeRepo()

        # Adding students to the student repository
        self.__studentRepo.add(Student(1, "Manulescu Andrei", 915))
        self.__studentRepo.add(Student(2, "Petraru Ioana", 915))
        self.__studentRepo.add(Student(3, "Rascolean Patricia", 916))
        self.__studentRepo.add(Student(4, "Bozea Alexandru", 918))
        self.__studentRepo.add(Student(5, "Popescu Ionut", 917))
        self.__studentRepo.add(Student(6, "George Michael", 920))
        self.__studentRepo.add(Student(7, "Tataru Diana", 918))
        self.__studentRepo.add(Student(8, "Andreica Daniel", 917))
        self.__studentRepo.add(Student(9, "Anghel George", 913))
        self.__studentRepo.add(Student(10, "Popescu Alexandru", 915))

        # Adding assignments to the assignment repository
        self.__assignmentRepo.add(Assignment(1, "Maths Homework", "13/10/2020"))
        self.__assignmentRepo.add(Assignment(2, "English Homework", "13/09/2020"))
        self.__assignmentRepo.add(Assignment(3, "Spanish Homework", "13/10/2020"))
        self.__assignmentRepo.add(Assignment(4, "Physics Homework", "13/11/2020"))
        self.__assignmentRepo.add(Assignment(5, "IT Homework", "13/12/2021"))
        self.__assignmentRepo.add(Assignment(6, "CSA Homework", "13/10/2020"))
        self.__assignmentRepo.add(Assignment(7, "FP Homework", "14/12/2020"))
        self.__assignmentRepo.add(Assignment(8, "CL Homework", "13/11/2020"))
        self.__assignmentRepo.add(Assignment(9, "Literature Homework", "10/12/2020"))
        self.__assignmentRepo.add(Assignment(10, "French Homework", "16/12/2020"))

        # Adding given assignments to the grade repository
        self.__gradeRepo.create_ungraded(Grade(2, 2, None))
        self.__gradeRepo.create_ungraded(Grade(5, 3, None))
        self.__gradeRepo.create_ungraded(Grade(6, 2, None))
        self.__gradeRepo.create_ungraded(Grade(8, 4, None))
        self.__gradeRepo.create_ungraded(Grade(9, 8, None))
        self.__gradeRepo.create_ungraded(Grade(10, 8, None))
        self.__gradeRepo.create_ungraded(Grade(5, 9, None))
        self.__gradeRepo.create_ungraded(Grade(8, 2, None))
        self.__gradeRepo.create_ungraded(Grade(10, 5, None))
        self.__gradeRepo.create_ungraded(Grade(5, 7, None))

        # Adding grades to the grade repository
        self.__gradeRepo.create_graded(Grade(1, 3, 2))
        self.__gradeRepo.create_graded(Grade(5, 2, 9.8))
        self.__gradeRepo.create_graded(Grade(8, 5, 10))
        self.__gradeRepo.create_graded(Grade(7, 6, 9))
        self.__gradeRepo.create_graded(Grade(9, 10, 8))
        self.__gradeRepo.create_graded(Grade(10, 7, 8))
        self.__gradeRepo.create_graded(Grade(5, 10, 6.3))
        self.__gradeRepo.create_graded(Grade(1, 2, 8))
        self.__gradeRepo.create_graded(Grade(1, 1, 7))
        self.__gradeRepo.create_graded(Grade(9, 7, 7))

    def __init_text_files(self, students, assignments, ungraded, graded):
        # initialising the text files repos in case we choose to use text files for reading data
        self.__studentRepo = FileStudentRepo(students)
        self.__assignmentRepo = FileAssignmentRepo(assignments)
        self.__gradeRepo = FileGradeRepo(ungraded, graded)

    def start(self):
        # kept the configuration in a properties file
        config = configparser.ConfigParser()
        config.read("settings.properties")

        if config["REPOS"]["repository"] == "inmemory":
            self.__init_inmemory()
        elif config["REPOS"]["repository"] == "text_files":
            self.__init_text_files(config["REPOS"]["students"], config["REPOS"]["assignments"],
                                   config["REPOS"]["ungraded"], config["REPOS"]["graded"])
        else:
            print("Invalid properties!")
            return

        studentValidator = StudentValidator()
        assignmentValidator = AssignmentValidator()
        gradeValidator = GradeValidator()
        undoRedoRepo = UndoRedoRepo(self.__studentRepo, self.__assignmentRepo, self.__gradeRepo)
        studentSrv = StudentService(studentValidator, self.__studentRepo, undoRedoRepo)
        assignmentSrv = AssignmentService(assignmentValidator, self.__assignmentRepo, undoRedoRepo)
        gradeSrv = GradeService(gradeValidator, self.__studentRepo, self.__assignmentRepo, self.__gradeRepo,
                                undoRedoRepo)
        undoRedoSrv = UndoRedoSrv(undoRedoRepo)
        console = UI(studentSrv, assignmentSrv, gradeSrv, undoRedoSrv)
        console.run()

