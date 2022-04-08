from datetime import datetime

from domain.entity import Student, Assignment, Grade, UndoRedoAction
from errors.exceptions import RepositoryException
import pickle


class StudentRepo:
    def __init__(self):
        self._elements = []

    def add(self, student):
        try:
            if student in self._elements is not None:
                raise RepositoryException("This student already exists!")
            self._elements.append(student)
        except TypeError:
            if student == self._elements:
                raise RepositoryException("This student already exists!")
            student1 = self._elements
            self._elements = []
            self._elements.append(student1)
            self._elements.append(student)

    def remove(self, student):
        """
        we check if this student exists and if yes then we look for him in the students list and then delete him
        :param student: the removed student
        :return:
        """
        try:
            if student not in self._elements:
                raise RepositoryException("This student doesn't exist!")
            for i in range(len(self._elements)):
                if self._elements[i] == student:
                    del self._elements[i]
                    return
        except TypeError:
            if student != self._elements:
                raise RepositoryException("This student doesn't exist!")
            self._elements = []

    def update(self, new_student):
        """
        we check to see if the student exists and if yes then we update his name and group with the given ones
        :param new_student: where we store the ID of the student we wanna update and the new info that we update with
        :return:
        """
        try:
            if new_student not in self._elements:
                raise RepositoryException("This student doesn't exist!")
            for i in range(len(self._elements)):
                if self._elements[i] == new_student:
                    self._elements[i].set_name(new_student.get_name())
                    self._elements[i].set_group(new_student.get_group())
                    return
        except TypeError:
            if new_student != self._elements:
                raise RepositoryException("This student doesn't exist!")
            self._elements.set_name(new_student.get_name())
            self._elements.set_group(new_student.get_group())

    def search(self, st_id):
        """
        Checks to see if a student already exists and then returns that student
        :param st_id: the id we are looking for
        :return:
        """
        student = Student(st_id, "name", 0)
        try:
            if student not in self._elements:
                raise RepositoryException("This student doesn't exist!")
            for el in self._elements:
                if el.get_st_id() == st_id:
                    return el
        except TypeError:
            if student != self._elements:
                raise RepositoryException("This student doesn't exist!")
            return self._elements

    def get_all(self):
        """
        :return: the list of all students added
        """
        return self._elements


class AssignmentRepo:
    def __init__(self):
        self._elements = []

    def add(self, assignment):
        """
        we check to see if this assignment exists and if not then we add it to the assignments list
        :param assignment: the added assignment
        :return:
        """
        try:
            if assignment in self._elements is not None:
                raise RepositoryException("This assignment already exists!")
            self._elements.append(assignment)
        except TypeError:
            if assignment == self._elements:
                raise RepositoryException("This assignment already exists!")
            elem = self._elements
            self._elements = []
            self._elements.append(elem)
            self._elements.append(assignment)

    def remove(self, assignment):
        """
        we check to see if this assignment exists and if yes then we look for it to remove it from the list
        :param assignment: the removes assignment
        :return:
        """
        try:
            if assignment not in self._elements:
                raise RepositoryException("This assignment doesn't exist!")
            for i in range(len(self._elements)):
                if self._elements[i] == assignment:
                    del self._elements[i]
                    return
        except TypeError:
            if assignment != self._elements:
                raise RepositoryException("This assignment doesn't exist!")
            self._elements = []

    def update(self, new_assignment):
        """
        we check to see if this assignment exists and if yes then we update it with new description and deadline
        :param new_assignment: where we store the ID of the assignment we wanna replace + the new info
        :return:
        """
        try:
            if new_assignment not in self._elements:
                raise RepositoryException("This student doesn't exist!")
            for i in range(len(self._elements)):
                if self._elements[i] == new_assignment:
                    self._elements[i].set_name(new_assignment.get_desc())
                    self._elements[i].set_group(new_assignment.get_dl())
                    return
        except TypeError:
            if new_assignment != self._elements:
                raise RepositoryException("This assignment doesn't exist!")
            self._elements.set_desc(new_assignment.get_desc())
            self._elements.set_dl(new_assignment.get_dl())

    def search(self, as_id):
        """
        Checks to see if an assignment already exists and then returns that student
        :param: the id we are looking for
        :return:
        """
        assignment = Assignment(as_id, "a", "a")
        try:
            if assignment not in self._elements:
                raise RepositoryException("This assignment doesn't exist!")
            for el in self._elements:
                if el.get_as_id() == as_id:
                    return el
        except TypeError:
            if assignment != self._elements:
                raise RepositoryException("This student doesn't exist!")
            return self._elements

    def check_if_late(self, assignment):
        """
        checks if the deadline has passed by comparing the date of the deadline with the current date
        :param assignment: the assignment whose deadline we are checking
        :return: True if late, False otherwise
        """
        current_day = datetime.now().day
        current_month = datetime.now().month
        current_year = datetime.now().year
        date = assignment.get_dl().split("/")
        if current_year > int(date[2]):
            return True
        elif current_year < int(date[2]):
            return False
        if current_month > int(date[1]):
            return True
        elif current_month < int(date[1]):
            return False
        if current_day > int(date[0]):
            return True
        else:
            return False

    def get_all(self):
        """
        :return: the list of all assignments added
        """
        return self._elements


class GradeRepo:

    def __init__(self):
        self._ungraded = []
        self._graded = []

    def create_ungraded(self, grade):
        """
        check to see if this student has been given this assignment before and if not then we add the grade to the list
        :param grade: where we store the ID of the student and the ID of the assignment we wanna give to that student
        :return:
        """
        try:
            if grade not in self._ungraded:
                grade.set_grade(None)
                self._ungraded.append(grade)
        except TypeError:
            if grade != self._ungraded:
                grade.set_grade(None)
                elem = self._ungraded
                self._ungraded = []
                self._ungraded.append(elem)
                self._ungraded.append(grade)

    def search_in_graded(self, st_id, as_id):
        """
        looks for a specific grade by the student id and assignment id
        :param st_id: the student id
        :param as_id: the assignment id
        :return:
        """
        grade = Grade(st_id, as_id, 0)
        try:
            if grade not in self._graded:
                raise RepositoryException("This assignment hasn't been graded yet!")
            for el in self._graded:
                if el == grade:
                    return el
        except TypeError:
            if grade != self._graded:
                raise RepositoryException("This assignment hasn't been graded yet!")
            return self._graded

    def search_in_ungraded(self, st_id, as_id):
        """
        same as search_in_graded but for ungraded assignments
        :param st_id: the student id
        :param as_id: the assignment id
        :return:
        """
        grade = Grade(st_id, as_id, 0)
        try:
            if grade not in self._ungraded:
                raise RepositoryException("This assignment hasn't been given yet!")
            for el in self._ungraded:
                if el == grade:
                    return el
        except TypeError:
            if grade != self._ungraded:
                raise RepositoryException("This assignment hasn't been given yet!")
            return self._ungraded

    def remove_from_ungraded(self, st_id, as_id):
        """
        removes a given assignment from the ungraded list
        :param st_id: student id
        :param as_id: assignment id
        :return:
        """
        grade = self.search_in_ungraded(st_id, as_id)
        try:
            for i in range(len(self._ungraded)):
                if self._ungraded[i] == grade:
                    del self._ungraded[i]
                    return
        except TypeError:
            self._ungraded = []

    def remove_from_graded(self, st_id, as_id):
        """
        removes a given assignment from the ungraded list
        :param st_id: student id
        :param as_id: assignment id
        :return:
        """
        grade = self.search_in_graded(st_id, as_id)
        try:
            for i in range(len(self._graded)):
                if self._graded[i] == grade:
                    del self._graded[i]
                    return
        except TypeError:
            self._graded = []

    def create_graded(self, grade):
        """
        Marks a given assignment with a grade
        :param grade: the grade we are creating
        :return:
        """
        try:
            if grade not in self._graded:
                self._graded.append(grade)
        except TypeError:
            if grade != self._graded:
                elem = self._graded
                self._graded = []
                self._graded.append(elem)
                self._graded.append(grade)

    def get_student_avg(self, st_id):
        """
        gets the average of all grades from each given assignment of a student
        :param st_id: the student id
        :return: the average i.e. the sum of the grades divided by the number of grades
        """
        grades = self.get_all_graded()
        avg_num = 0
        avg_sum = 0
        try:
            for grade in grades:
                if grade.get_st_id() == st_id:
                    avg_num += 1
                    avg_sum += grade.get_grade()
            if avg_num == 0:
                return 0
        except TypeError:
            if grades.get_st_id() == st_id:
                avg_sum = grades.get_grade()
                avg_num = 1
            else:
                return 0
        return avg_sum/avg_num

    def get_all_ungraded(self):
        """
        :return: the list of all given assignments (so the ones that haven't been graded yet)
        """
        return self._ungraded

    def list_of_graded_for_assignment(self, as_id):
        """
        makes the list of grades for an assignment
        :param as_id: the assignment id
        :return:
        """
        lst = []
        try:
            for grade in self._graded:
                if grade.get_as_id() == as_id:
                    lst.append(grade)
        except TypeError:
            if self._graded.get_as_id() == as_id:
                lst.append(self._graded)
        return lst

    def list_of_ungraded_for_assignment(self, as_id):
        """
        makes the list of ungraded students for a given assignment
        :param as_id: the assignment id
        :return:
        """
        lst = []
        try:
            for grade in self._ungraded:
                if grade.get_as_id() == as_id:
                    lst.append(grade)
        except TypeError:
            if self._ungraded.get_as_id() == as_id:
                lst.append(self._ungraded)
        return lst

    def get_all_graded(self):
        """
        list of all graded assignments
        :return:
        """
        return self._graded


class UndoRedoRepo:

    def __init__(self, studentRepo, assignmentRepo, gradeRepo):
        self.__elements = []
        self.__studentRepo = studentRepo
        self.__assignmentRepo = assignmentRepo
        self.__gradeRepo = gradeRepo
        self.__undone_list = []

    def empty_list(self):
        self.__undone_list = []

    def add_action(self, action, obj):
        undoRedoAction = UndoRedoAction(action, obj)
        self.__elements.append(undoRedoAction)

    def reverse_add_student(self, student):
        self.__studentRepo.remove(student)
        element = self.__elements.pop()
        self.__undone_list.append(element)

    def reverse_remove_student(self, student):
        self.__studentRepo.add(student)
        element = self.__elements[-1]
        self.__undone_list.append(element)

    def reverse_remove_assignments(self, list_grades):
        for element in list_grades:
            if element.get_grade() is None:
                self.__gradeRepo.create_ungraded(element)
            else:
                self.__gradeRepo.create_graded(element)
        element = self.__elements.pop()
        self.__undone_list.append(element)

    def reverse_update_student(self, updates):
        self.__studentRepo.update(updates[0])
        element = self.__elements.pop()
        self.__undone_list.append(element)

    def reverse_add_assignment(self, assignment):
        self.__assignmentRepo.remove(assignment)
        element = self.__elements.pop()
        self.__undone_list.append(element)

    def reverse_remove_assignment(self, assignment):
        self.__assignmentRepo.add(assignment)
        element = self.__elements[-1]
        self.__undone_list.append(element)

    def reverse_remove_grades(self, list_grades):
        for element in list_grades:
            if element.get_grade() is None:
                self.__gradeRepo.create_ungraded(element)
            else:
                self.__gradeRepo.create_graded(element)
        element = self.__elements.pop()
        self.__undone_list.append(element)

    def reverse_update_assignment(self, updates):
        self.__studentRepo.update(updates[0])
        element = self.__elements.pop()
        self.__undone_list.append(element)

    def reverse_give_assignment(self, given_assignment):
        self.__gradeRepo.remove_from_ungraded(given_assignment.get_st_id(), given_assignment.get_as_id())
        element = self.__elements.pop()
        self.__undone_list.append(element)

    def reverse_give_assignment_to_group(self, given_list):
        for element in given_list:
            self.__gradeRepo.remove_from_ungraded(element.get_st_id(), element.get_as_id())
        element = self.__elements.pop()
        self.__undone_list.append(element)

    def reverse_grade_student(self, grade):
        self.__gradeRepo.create_ungraded(grade)
        self.__gradeRepo.remove_from_graded(grade.get_st_id(), grade.get_as_id())
        element = self.__elements.pop()
        self.__undone_list.append(element)

    def add_student(self, student):
        self.__studentRepo.add(student)
        self.__undone_list.pop()

    def remove_student(self, student):
        self.__studentRepo.remove(student)
        self.__undone_list.pop()

    def remove_assignments(self, list_grades):
        for element in list_grades:
            if element.get_grade() is None:
                self.__gradeRepo.remove_from_ungraded(element.get_st_id(), element.get_as_id())
            else:
                self.__gradeRepo.remove_from_graded(element.get_st_id(), element.get_as_id())
        # self.__undone_list.pop()

    def update_student(self, updates):
        self.__studentRepo.update(updates[1])
        self.__undone_list.pop()

    def add_assignment(self, assignment):
        self.__assignmentRepo.add(assignment)
        self.__undone_list.pop()

    def remove_assignment(self, assignment):
        self.__assignmentRepo.remove(assignment)
        self.__undone_list.pop()

    def remove_grades(self, list_grades):
        for element in list_grades:
            if element.get_grade() is None:
                self.__gradeRepo.remove_from_ungraded(element.get_st_id(), element.get_as_id())
            else:
                self.__gradeRepo.remove_from_graded(element.get_st_id(), element.get_as_id())
        # self.__undone_list.pop()

    def update_assignment(self, updates):
        self.__studentRepo.update(updates[1])
        self.__undone_list.pop()

    def give_assignment(self, given_assignment):
        self.__gradeRepo.create_ungraded(given_assignment)
        self.__undone_list.pop()

    def give_assignment_to_group(self, given_list):
        for element in given_list:
            self.__gradeRepo.create_ungraded(element)
        self.__undone_list.pop()

    def grade_student(self, grade):
        self.__gradeRepo.remove_from_ungraded(grade.get_st_id(), grade.get_as_id())
        self.__gradeRepo.create_graded(grade)
        self.__undone_list.pop()

    def get_all_actions(self):
        return self.__elements

    def get_all_undone(self):
        return self.__undone_list


class FileStudentRepo(StudentRepo):
    def __init__(self, txt):
        self.__txt = txt
        StudentRepo.__init__(self)

    def __read_students_from_file(self):
        with open(self.__txt, "r") as f:
            self._elements = []
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line != "":
                    line.strip()
                    parts = line.split(";")
                    student = Student(int(parts[0]), parts[1], int(parts[2]))
                    self._elements.append(student)
        f.close()

    def __write_students_in_file(self):
        with open(self.__txt, "w") as f:
            students = self._elements
            for student in students:
                f.write(str(student.get_st_id())+";"+student.get_name()+";"+str(student.get_group())+"\n")

    def add(self, student):
        self.__read_students_from_file()
        StudentRepo.add(self, student)
        self.__write_students_in_file()

    def remove(self, student):
        self.__read_students_from_file()
        StudentRepo.remove(self, student)
        self.__write_students_in_file()

    def update(self, new_student):
        self.__read_students_from_file()
        StudentRepo.update(self, new_student)
        self.__write_students_in_file()

    def search(self, st_id):
        self.__read_students_from_file()
        return StudentRepo.search(self, st_id)

    def get_all(self):
        self.__read_students_from_file()
        return StudentRepo.get_all(self)


class FileAssignmentRepo(AssignmentRepo):
    def __init__(self, txt):
        self.__txt = txt
        AssignmentRepo.__init__(self)

    def __read_assignments_from_file(self):
        with open(self.__txt, "r") as f:
            self._elements = []
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line != "":
                    parts = line.split(";")
                    assignment = Assignment(int(parts[0]), parts[1], parts[2])
                    self._elements.append(assignment)
        f.close()

    def __write_assignments_in_file(self):
        with open(self.__txt, "w") as f:
            assignments = self._elements
            for assignment in assignments:
                f.write(str(assignment.get_as_id())+";"+assignment.get_desc()+";"+assignment.get_dl()+"\n")

    def add(self, assignment):
        self.__read_assignments_from_file()
        AssignmentRepo.add(self, assignment)
        self.__write_assignments_in_file()

    def remove(self, assignment):
        self.__read_assignments_from_file()
        AssignmentRepo.remove(self, assignment)
        self.__write_assignments_in_file()

    def update(self, new_assignment):
        self.__read_assignments_from_file()
        AssignmentRepo.update(self, new_assignment)
        self.__write_assignments_in_file()

    def search(self, as_id):
        self.__read_assignments_from_file()
        return AssignmentRepo.search(self, as_id)

    def check_if_late(self, assignment):
        self.__read_assignments_from_file()
        return AssignmentRepo.check_if_late(self, assignment)

    def get_all(self):
        self.__read_assignments_from_file()
        return AssignmentRepo.get_all(self)


class FileGradeRepo(GradeRepo):
    def __init__(self, ungraded, graded):
        self.__ungraded_file = ungraded
        self.__graded_file = graded
        GradeRepo.__init__(self)

    def __read_ungraded_from_file(self):
        with open(self.__ungraded_file, "r") as f:
            self._ungraded = []
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line != "":
                    parts = line.split(";")
                    grade = Grade(int(parts[0]), int(parts[1]), None)
                    self._ungraded.append(grade)
        f.close()

    def __read_graded_from_file(self):
        with open(self.__graded_file, "r") as f:
            self._graded = []
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line != "":
                    line.strip()
                    parts = line.split(";")
                    grade = Grade(int(parts[0]), int(parts[1]), float(parts[2]))
                    self._graded.append(grade)
        f.close()

    def __write_ungraded_in_file(self):
        with open(self.__ungraded_file, "w") as f:
            for ungraded in self._ungraded:
                f.write(str(ungraded.get_st_id())+";"+str(ungraded.get_as_id())+";"+str(ungraded.get_grade())+"\n")

    def __write_graded_in_file(self):
        with open(self.__graded_file, "w") as f:
            for graded in self._graded:
                f.write(str(graded.get_st_id())+";"+str(graded.get_as_id())+";"+str(graded.get_grade())+"\n")

    def create_ungraded(self, grade):
        self.__read_ungraded_from_file()
        GradeRepo.create_ungraded(self, grade)
        self.__write_ungraded_in_file()

    def create_graded(self, grade):
        self.__read_graded_from_file()
        GradeRepo.create_graded(self, grade)
        self.__write_graded_in_file()

    def search_in_graded(self, st_id, as_id):
        self.__read_graded_from_file()
        return GradeRepo.search_in_graded(self, st_id, as_id)

    def search_in_ungraded(self, st_id, as_id):
        self.__read_ungraded_from_file()
        return GradeRepo.search_in_ungraded(self, st_id, as_id)

    def remove_from_ungraded(self, st_id, as_id):
        self.__read_ungraded_from_file()
        GradeRepo.remove_from_ungraded(self, st_id, as_id)
        self.__write_ungraded_in_file()

    def remove_from_graded(self, st_id, as_id):
        self.__read_graded_from_file()
        GradeRepo.remove_from_graded(self, st_id, as_id)
        self.__write_graded_in_file()

    def get_student_avg(self, st_id):
        self.__read_graded_from_file()
        return GradeRepo.get_student_avg(self, st_id)

    def get_all_ungraded(self):
        self.__read_ungraded_from_file()
        return GradeRepo.get_all_ungraded(self)

    def list_of_graded_for_assignment(self, as_id):
        self.__read_graded_from_file()
        return GradeRepo.list_of_graded_for_assignment(self, as_id)

    def list_of_ungraded_for_assignment(self, as_id):
        self.__read_ungraded_from_file()
        return GradeRepo.list_of_ungraded_for_assignment(self, as_id)

    def get_all_graded(self):
        self.__read_graded_from_file()
        return GradeRepo.get_all_graded(self)


class BinaryStudentRepo(StudentRepo):
    def __init__(self, txt):
        self.__txt = txt
        StudentRepo.__init__(self)

    def __read_students_from_file(self):
        with open(self.__txt, "rb") as f:
            try:
                self._elements = pickle.load(f)
            except EOFError:
                self._elements = []

    def __write_students_in_file(self):
        with open(self.__txt, "wb") as f:
            students = self._elements
            pickle.dump(students, f)

    def add(self, student):
        self.__read_students_from_file()
        StudentRepo.add(self, student)
        self.__write_students_in_file()

    def remove(self, student):
        self.__read_students_from_file()
        StudentRepo.remove(self, student)
        self.__write_students_in_file()

    def update(self, new_student):
        self.__read_students_from_file()
        StudentRepo.update(self, new_student)
        self.__write_students_in_file()

    def search(self, st_id):
        self.__read_students_from_file()
        return StudentRepo.search(self, st_id)

    def get_all(self):
        self.__read_students_from_file()
        return StudentRepo.get_all(self)


class BinaryAssignmentRepo(AssignmentRepo):
    def __init__(self, txt):
        self.__txt = txt
        AssignmentRepo.__init__(self)

    def __read_assignments_from_file(self):
        with open(self.__txt, "rb") as f:
            try:
                self._elements = pickle.load(f)
            except EOFError:
                self._elements = []

    def __write_assignments_in_file(self):
        with open(self.__txt, "wb") as f:
            assignments = self._elements
            pickle.dump(assignments, f)

    def add(self, assignment):
        self.__read_assignments_from_file()
        AssignmentRepo.add(self, assignment)
        self.__write_assignments_in_file()

    def remove(self, assignment):
        self.__read_assignments_from_file()
        AssignmentRepo.remove(self, assignment)
        self.__write_assignments_in_file()

    def update(self, new_assignment):
        self.__read_assignments_from_file()
        AssignmentRepo.update(self, new_assignment)
        self.__write_assignments_in_file()

    def search(self, as_id):
        self.__read_assignments_from_file()
        return AssignmentRepo.search(self, as_id)

    def check_if_late(self, assignment):
        self.__read_assignments_from_file()
        return AssignmentRepo.check_if_late(self, assignment)

    def get_all(self):
        self.__read_assignments_from_file()
        return AssignmentRepo.get_all(self)


class BinaryGradeRepo(GradeRepo):
    def __init__(self, ungraded, graded):
        self.__ungraded_file = ungraded
        self.__graded_file = graded
        GradeRepo.__init__(self)

    def __read_ungraded_from_file(self):
        with open(self.__ungraded_file, "rb") as f:
            try:
                self._ungraded = pickle.load(f)
            except EOFError:
                self._ungraded = []

    def __read_graded_from_file(self):
        with open(self.__graded_file, "rb") as f:
            try:
                self._graded = pickle.load(f)
            except EOFError:
                self._graded = []

    def __write_ungraded_in_file(self):
        with open(self.__ungraded_file, "wb") as f:
            pickle.dump(self._ungraded, f)

    def __write_graded_in_file(self):
        with open(self.__graded_file, "wb") as f:
            pickle.dump(self._graded, f)

    def create_ungraded(self, grade):
        self.__read_ungraded_from_file()
        GradeRepo.create_ungraded(self, grade)
        self.__write_ungraded_in_file()

    def create_graded(self, grade):
        self.__read_graded_from_file()
        GradeRepo.create_graded(self, grade)
        self.__write_graded_in_file()

    def search_in_graded(self, st_id, as_id):
        self.__read_graded_from_file()
        return GradeRepo.search_in_graded(self, st_id, as_id)

    def search_in_ungraded(self, st_id, as_id):
        self.__read_ungraded_from_file()
        return GradeRepo.search_in_ungraded(self, st_id, as_id)

    def remove_from_ungraded(self, st_id, as_id):
        self.__read_ungraded_from_file()
        GradeRepo.remove_from_ungraded(self, st_id, as_id)
        self.__write_ungraded_in_file()

    def remove_from_graded(self, st_id, as_id):
        self.__read_graded_from_file()
        GradeRepo.remove_from_graded(self, st_id, as_id)
        self.__write_graded_in_file()

    def get_student_avg(self, st_id):
        self.__read_graded_from_file()
        return GradeRepo.get_student_avg(self, st_id)

    def get_all_ungraded(self):
        self.__read_ungraded_from_file()
        return GradeRepo.get_all_ungraded(self)

    def list_of_graded_for_assignment(self, as_id):
        self.__read_graded_from_file()
        return GradeRepo.list_of_graded_for_assignment(self, as_id)

    def list_of_ungraded_for_assignment(self, as_id):
        self.__read_ungraded_from_file()
        return GradeRepo.list_of_ungraded_for_assignment(self, as_id)

    def get_all_graded(self):
        self.__read_graded_from_file()
        return GradeRepo.get_all_graded(self)
