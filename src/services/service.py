from domain.entity import Student, Assignment, Grade
from domain.auxil import selection_sort


class StudentService:

    def __init__(self, studentValidator, studentRepo, undoRedoRepo):
        """
        initialise the service
        :param studentValidator: the student validator we will use
        :param studentRepo: the student repository we will use
        """
        self.__studentValidator = studentValidator
        self.__studentRepo = studentRepo
        self.__undoRedoRepo = undoRedoRepo

    def add_student(self, st_id, name, group):
        """
        creates a student with the given info, validates the student and then uses the add method
        :param st_id: the student ID
        :param name: the student's Name
        :param group: the student's Group
        :return:
        """
        student = Student(st_id, name, group)
        self.__studentValidator.validate(student)
        self.__studentRepo.add(student)
        self.__undoRedoRepo.add_action("add_student", student)
        self.__undoRedoRepo.empty_list()

    def remove_student(self, st_id):
        """
        creates a student key with the given ID to use when removing the student since all that's important is the ID
        and then uses the remove method
        :param st_id: the ID of the student we will remove
        :return:
        """
        student_key = Student(st_id, "name", 915)
        student = self.__studentRepo.search(st_id)
        self.__studentRepo.remove(student_key)
        self.__undoRedoRepo.add_action("remove_student", student)
        self.__undoRedoRepo.empty_list()

    def update_student(self, st_id, new_name, new_group):
        """
        creates a new student with the given ID, the new given name and the new given group, and then uses the
        update method
        :param st_id: the ID of the student we shall update
        :param new_name: his new name
        :param new_group: his new group
        :return:
        """
        student = self.__studentRepo.search(st_id)
        new_student = Student(st_id, new_name, new_group)
        updates = [student, new_student]
        self.__studentRepo.update(new_student)
        self.__undoRedoRepo.add_action("update_student", updates)
        self.__undoRedoRepo.empty_list()

    def list_students(self):
        """
        gets the list of all students and then prints each element consecutively
        :return:
        """
        students_list = self.__studentRepo.get_all()
        if len(students_list) == 0:
            print("There is nothing to list!")
            return
        print("--------------------------------"
              "\nThe list of all students:")
        for student in students_list:
            print(str(student))
        print("--------------------------------")


class AssignmentService:

    def __init__(self, assignmentValidator, assignmentRepo, undoRedoRepo):
        """
        initialise the service
        :param assignmentValidator: the assignment validator we will use
        :param assignmentRepo: the assignment repository we will use
        """
        self.__assignmentValidator = assignmentValidator
        self.__assignmentRepo = assignmentRepo
        self.__undoRedoRepo = undoRedoRepo

    def add_assignment(self, as_id, desc, dl):
        """
        creates the assignment, validates it and then uses the add method to add the created assignment
        :param as_id: the assignment ID
        :param desc: the assignment description
        :param dl: the assignment deadline
        :return:
        """
        assignment = Assignment(as_id, desc, dl)
        self.__assignmentValidator.validate(assignment)
        self.__assignmentRepo.add(assignment)
        self.__undoRedoRepo.add_action("add_assignment", assignment)
        self.__undoRedoRepo.empty_list()

    def remove_assignment(self, as_id):
        """
        creates an assignment key using the given ID and then removes the assignment with that ID using the remove
        method
        :param as_id: the ID of the assignment we will remove
        :return:
        """
        assignment_key = Assignment(as_id, "desc", "deadline")
        assignment = self.__assignmentRepo.search(as_id)
        self.__assignmentRepo.remove(assignment_key)
        self.__undoRedoRepo.add_action("remove_assignment", assignment)
        self.__undoRedoRepo.empty_list()

    def update_assignment(self, as_id, new_desc, new_dl):
        """
        creates a new assignment with the old ID, a new description and a new deadline that will be used to
        update the assignment with that ID, using the update method
        :param as_id: the ID of the assignment we will update
        :param new_desc: the new description
        :param new_dl: the new deadline
        :return:
        """
        assignment = self.__assignmentRepo.search(as_id)
        new_assignment = Assignment(as_id, new_desc, new_dl)
        self.__assignmentRepo.update(new_assignment)
        updates = [assignment, new_assignment]
        self.__undoRedoRepo.add_action("update_assignment", updates)
        self.__undoRedoRepo.empty_list()

    def list_assignments(self):
        """
        gets the list of the added assignments and then prints each assignment consecutively
        :return:
        """
        assignments_list = self.__assignmentRepo.get_all()
        if len(assignments_list) == 0:
            print("There is nothing to list!")
            return
        print("--------------------------------"
              "\nThe list of all assignments:")
        for assignment in assignments_list:
            print(str(assignment))
        print("--------------------------------")


class GradeService:

    def __init__(self, gradeValidator, studentRepo, assignmentRepo, gradeRepo, undoRedoRepo):
        """

        :param gradeValidator: the Validator we will use
        :param studentRepo: the student repository we need for giving the assignment to one of its students
        :param assignmentRepo: the assignment repository we need for giving one of its assignments to a student
        :param gradeRepo: the grade repository we will need
        """
        self.__gradeValidator = gradeValidator
        self.__studentRepo = studentRepo
        self.__assignmentRepo = assignmentRepo
        self.__gradeRepo = gradeRepo
        self.__undoRedoRepo = undoRedoRepo

    def give_assignment_to_student(self, st_id, as_id, grade):
        """
        it makes the connection between a student and an assignment if they exist and then uses the create method
        :param st_id: the student we wanna give the assignment to
        :param as_id: the assignment we wanna give to the student
        :param grade: the grade which will be None for now, as we only care about the connection between the student
        and the given assignment
        :return:
        """
        student = self.__studentRepo.search(st_id)
        assignment = self.__assignmentRepo.search(as_id)
        given_assignment = Grade(st_id, as_id, grade)
        ungraded = self.__gradeRepo.get_all_ungraded()
        graded = self.__gradeRepo.get_all_graded()
        try:
            if given_assignment in graded:
                print("this assignment has already been given and graded to this student!")
                return
        except TypeError:
            if given_assignment == graded:
                print("this assignment has already been given and graded to this student!")
                return
        try:
            if given_assignment in ungraded:
                print("this assignment has already been given to this student!")
                return
        except TypeError:
            if given_assignment == ungraded:
                print("this assignment has already been given to this student!")
                return
        self.__gradeRepo.create_ungraded(given_assignment)
        self.__undoRedoRepo.add_action("give_assignment", given_assignment)
        self.__undoRedoRepo.empty_list()

    def give_assignment_to_group(self, group, as_id, grade):
        """
        it checks to see which students are in the given group and then calls the give_assignment_to_student method
        for each of those students
        :param group: the group of the students we will assign the homework to
        :param as_id: the assignment ID
        :param grade: the grade which will be None for now, as we only care about the connection between the student
        and the given assignment
        :return:
        """
        assignment = self.__assignmentRepo.search(as_id)
        ungraded = self.__gradeRepo.get_all_ungraded()
        graded = self.__gradeRepo.get_all_graded()
        assignment_list = []
        try:
            for student in self.__studentRepo.get_all():
                if student.get_group() == group:
                    given_assignment = Grade(student.get_st_id(), as_id, grade)
                    if given_assignment not in ungraded and given_assignment not in graded:
                        assignment_list.append(given_assignment)
                        self.__gradeRepo.create_ungraded(given_assignment)
        except TypeError:
            if self.__studentRepo.get_all().get_group() == group:
                given_assignment = Grade(self.__studentRepo.get_all().get_st_id(), as_id, grade)
                if given_assignment != ungraded and given_assignment != graded:
                    assignment_list.append(given_assignment)
                    self.__gradeRepo.create_ungraded(given_assignment)
        self.__undoRedoRepo.add_action("give_assignment_to_group", assignment_list)
        self.__undoRedoRepo.empty_list()

    def list_ungraded(self):
        """
        it creates the list of all ungraded students (all students and the assignments they have been given) and then
        prints each one of them
        :return:
        """
        ungraded_list = self.__gradeRepo.get_all_ungraded()
        if len(ungraded_list) == 0:
            print("There is nothing to list!")
            return
        print("--------------------------------"
              "\nThe list of all ungraded:")
        for ungraded in ungraded_list:
            print(str(ungraded))
        print("--------------------------------")

    def list_graded(self):
        """
        checks if there is any element in the list and prints them if so
        :return:
        """
        graded_list = self.__gradeRepo.get_all_graded()
        if len(graded_list) == 0:
            print("There is nothing to list!")
            return
        print("--------------------------------"
              "\nThe list of all ungraded:")
        for graded in graded_list:
            print(str(graded))
        print("--------------------------------")

    def list_ungraded_for_student(self, st_id):
        """
        checks if the student exists then takes the list of all ungraded assignments and prints the ones of the student
        :param st_id: the student we are listing for
        :return: true if there are ungraded assignments, false otherwise
        """
        student = self.__studentRepo.search(st_id)
        ungraded_list = self.__gradeRepo.get_all_ungraded()
        if len(ungraded_list) == 0:
            print("There is nothing to list!")
            return False
        print("--------------------------------"
              "\nThe list of all given assignments for student", st_id, "is:")
        k = False
        for grade in ungraded_list:
            if grade.get_st_id() == st_id:
                assignment = self.__assignmentRepo.search(grade.get_as_id())
                print(str(assignment))
                k = True
        print("--------------------------------")
        if k is False:
            print("This student hasn't been given any assignments yet! ")
            return False
        else:
            return True

    def list_graded_for_student(self, st_id):
        """
        checks if the student exists then takes the list of all graded assignments and prints the ones of the student
        :param st_id: the student we are listing for
        :return: true if there are ungraded assignments, false otherwise
        """
        student = self.__studentRepo.search(st_id)
        graded_list = self.__gradeRepo.get_all_graded()
        if len(graded_list) == 0:
            print("There is nothing to list!")
            return False
        print("--------------------------------"
              "\nThe list of all graded assignments for student", st_id, "is:")
        k = False
        for grade in graded_list:
            if grade.get_st_id() == st_id:
                assignment = self.__assignmentRepo.search(grade.get_as_id())
                print(str(assignment))
                k = True
        print("--------------------------------")
        if k is False:
            print("This student doesn't have any graded assignments yet! ")
            return False
        else:
            return True

    def grade_student(self, st_id, as_id, value):
        """
        grades an already existing given assignment
        :param st_id: the student id
        :param as_id: the assignment id
        :param value: the grade value
        :return:
        """
        assignment = self.__assignmentRepo.search(as_id)
        grade = self.__gradeRepo.search_in_ungraded(st_id, as_id)
        grade.set_grade(value)
        self.__gradeValidator.validate(grade)
        self.__gradeRepo.create_graded(grade)
        self.__gradeRepo.remove_from_ungraded(st_id, as_id)
        self.__undoRedoRepo.add_action("grade_student", grade)
        self.__undoRedoRepo.empty_list()

    def remove_assignments_of_student(self, st_id):
        """
        removes all given/graded assignments of a student
        :param st_id: the student's id
        :return:
        """
        graded_list = self.__gradeRepo.get_all_graded()
        ungraded_list = self.__gradeRepo.get_all_ungraded()
        removed_list = []
        for i in reversed(range(len(graded_list))):
            if graded_list[i].get_st_id() == st_id:
                removed_list.append(graded_list[i])
                del graded_list[i]
        for i in reversed(range(len(ungraded_list))):
            if ungraded_list[i].get_st_id() == st_id:
                removed_list.append(ungraded_list[i])
                del ungraded_list[i]
        self.__undoRedoRepo.add_action("remove_assignments", removed_list)
        self.__undoRedoRepo.empty_list()

    def remove_grades_of_assignment(self, as_id):
        """
        removes all grades given for an assignment for every student
        :param as_id: the assignment id
        :return:
        """
        graded_list = self.__gradeRepo.get_all_graded()
        ungraded_list = self.__gradeRepo.get_all_ungraded()
        removed_list = []
        for i in reversed(range(len(graded_list))):
            if graded_list[i].get_as_id() == as_id:
                removed_list.append(graded_list[i])
                del graded_list[i]
        for i in reversed(range(len(ungraded_list))):
            if ungraded_list[i].get_as_id() == as_id:
                removed_list.append(ungraded_list[i])
                del ungraded_list[i]
        self.__undoRedoRepo.add_action("remove_grades", removed_list)
        self.__undoRedoRepo.empty_list()

    def list_ordered_for_assignment(self, as_id):
        """
        orders the list of graded students for this assignment and prints it + prints the ungraded students
        :param as_id: the assignment id
        :return:
        """
        graded_list = self.__gradeRepo.list_of_graded_for_assignment(as_id)
        ungraded_list = self.__gradeRepo.list_of_ungraded_for_assignment(as_id)
        graded_list.sort(key=lambda x: x.get_grade())
        if len(graded_list) + len(ungraded_list) == 0:
            print("There is nothing to list!")
            return
        if len(graded_list) == 0:
            print("\nThere are no graded students for this assignment")
        else:
            print("--------------------------------"
                  "\nThe list of students for assignment", as_id, "ordered: ")
            for grade in graded_list:
                student = self.__studentRepo.search(grade.get_st_id())
                assignment = self.__assignmentRepo.search(grade.get_as_id())
                print(str(student) + " with the grade:", grade.get_grade())
        if len(ungraded_list) == 0:
            print("\nThere are no ungraded students for this assignment")
        else:
            print("--------------------------------"
                  "\nThe list of ungraded students for assignment", as_id, "is: ")
            for grade in ungraded_list:
                student = self.__studentRepo.search(grade.get_st_id())
                print(str(student))
        print("--------------------------------")

    def list_late_students(self):
        """
        makes the list of all late students by checking if the deadline has passed for any of their assignments
        :return:
        """
        lst = []
        ungraded_list = self.__gradeRepo.get_all_ungraded()
        for grade in ungraded_list:
            assignment = self.__assignmentRepo.search(grade.get_as_id())
            if self.__assignmentRepo.check_if_late(assignment):
                student = self.__studentRepo.search(grade.get_st_id())
                if student not in lst:
                    lst.append(student)
        print("--------------------------------"
              "\nThe list of all late students is: ")
        for student in lst:
            print(str(student))
        print("--------------------------------")

    def order_by_avg_grade(self):
        """
        sorts the list of students by their avg grade of all the assignments and then prints it
        :return:
        """
        students = self.__studentRepo.get_all()
        if len(students) == 0:
            print("There is nothing to list!")
        # students.sort(reverse=True, key=lambda x: self.__gradeRepo.get_student_avg(x.get_st_id()))
        selection_sort(students, key=lambda x: self.__gradeRepo.get_student_avg(x.get_st_id()))
        students = reversed(students)
        print("--------------------------------"
              "\nThe list of students sorted by best school average: ")
        for student in students:
            st_avg = self.__gradeRepo.get_student_avg(student.get_st_id())
            if st_avg > 0:
                print(str(student) + " with an average of: ", st_avg)
            if st_avg == 0:
                print(str(student) + " doesn't have any grades yet")
        print("--------------------------------")


class UndoRedoSrv:
    def __init__(self, undoRedoRepo):
        self.__undoRedoRepo = undoRedoRepo

    def undo_last_action(self):
        # in order to undo an option we keep all the done actions in a list,
        # and then do the reverse action based on what information we have
        actions_list = self.__undoRedoRepo.get_all_actions()
        if len(actions_list) == 0:
            print("There is nothing to undo!")
            return
        last_action = actions_list[-1]
        if last_action.get_action() == "add_student":
            self.__undoRedoRepo.reverse_add_student(last_action.get_object())
        elif last_action.get_action() == "remove_student":
            self.__undoRedoRepo.reverse_remove_student(last_action.get_object())
            actions_list.pop()
            last_action = actions_list[-1]
            self.__undoRedoRepo.reverse_remove_assignments(last_action.get_object())
        elif last_action.get_action() == "update_student":
            self.__undoRedoRepo.reverse_update_student(last_action.get_object())
        elif last_action.get_action() == "add_assignment":
            self.__undoRedoRepo.reverse_add_assignment(last_action.get_object())
        elif last_action.get_action() == "remove_assignment":
            self.__undoRedoRepo.reverse_remove_assignment(last_action.get_object())
            actions_list.pop()
            last_action = actions_list[-1]
            self.__undoRedoRepo.reverse_remove_grades(last_action.get_object())
        elif last_action.get_action() == "update_assignment":
            self.__undoRedoRepo.reverse_update_assignment(last_action.get_object())
        elif last_action.get_action() == "give_assignment":
            self.__undoRedoRepo.reverse_give_assignment(last_action.get_object())
        elif last_action.get_action() == "give_assignment_to_group":
            self.__undoRedoRepo.reverse_give_assignment_to_group(last_action.get_object())
        elif last_action.get_action() == "grade_student":
            self.__undoRedoRepo.reverse_grade_student(last_action.get_object())

    def redo_last_action(self):
        # in order to redo an option we keep all the undone actions in a list
        # and then we take the last undone action to redo it again based on the information we have
        actions_list = self.__undoRedoRepo.get_all_undone()
        if len(actions_list) == 0:
            print("There is nothing to redo!")
            return
        last_action = actions_list[-1]

        if last_action.get_action() == "add_student":
            self.__undoRedoRepo.add_student(last_action.get_object())
            self.__undoRedoRepo.add_action(last_action.get_action(), last_action.get_object())
        elif last_action.get_action() == "remove_assignments":
            self.__undoRedoRepo.remove_assignments(last_action.get_object())
            self.__undoRedoRepo.add_action(last_action.get_action(), last_action.get_object())
            actions_list.pop()
            last_action = actions_list[-1]
            self.__undoRedoRepo.remove_student(last_action.get_object())
            self.__undoRedoRepo.add_action(last_action.get_action(), last_action.get_object())
        elif last_action.get_action() == "update_student":
            self.__undoRedoRepo.update_student(last_action.get_object())
            self.__undoRedoRepo.add_action(last_action.get_action(), last_action.get_object())
        elif last_action.get_action() == "add_assignment":
            self.__undoRedoRepo.add_assignment(last_action.get_object())
            self.__undoRedoRepo.add_action(last_action.get_action(), last_action.get_object())
        elif last_action.get_action() == "remove_assignment":
            self.__undoRedoRepo.remove_grades(last_action.get_object())
            self.__undoRedoRepo.add_action(last_action.get_action(), last_action.get_object())
            actions_list.pop()
            last_action = actions_list[-1]
            self.__undoRedoRepo.remove_assignment(last_action.get_object())
            self.__undoRedoRepo.add_action(last_action.get_action(), last_action.get_object())
        elif last_action.get_action() == "update_assignment":
            self.__undoRedoRepo.update_assignment(last_action.get_object())
            self.__undoRedoRepo.add_action(last_action.get_action(), last_action.get_object())
        elif last_action.get_action() == "give_assignment":
            self.__undoRedoRepo.give_assignment(last_action.get_object())
            self.__undoRedoRepo.add_action(last_action.get_action(), last_action.get_object())
        elif last_action.get_action() == "give_assignment_to_group":
            self.__undoRedoRepo.give_assignment_to_group(last_action.get_object())
            self.__undoRedoRepo.add_action(last_action.get_action(), last_action.get_object())
        elif last_action.get_action() == "grade_student":
            self.__undoRedoRepo.grade_student(last_action.get_object())
            self.__undoRedoRepo.add_action(last_action.get_action(), last_action.get_object())
