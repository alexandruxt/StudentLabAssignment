from domain.validators import ValidatorError
from errors.exceptions import RepositoryException


def print_menu_options():
    print("\n"
          "Hello! Please choose an option:\n"
          "1 - Manage students\n"
          "2 - Manage assignments\n"
          "3 - Give assignments\n"
          "4 - Grade assignments\n"
          "5 - Show statistics\n"
          "6 - Undo last action\n"
          "7 - Redo last action\n"
          "x - Exit\n")


def print_options1():
    print("\n"
          "MANAGE STUDENTS:\n"
          "1 - Add student\n"
          "2 - Remove student\n"
          "3 - Update student\n"
          "4 - List students\n")


def print_options2():
    print("\n"
          "MANAGE ASSIGNMENTS:\n"
          "1 - Add assignment\n"
          "2 - Remove assignment\n"
          "3 - Update assignment\n"
          "4 - List assignments\n")


def print_options3():
    print("\n"
          "GIVE ASSIGNMENTS:\n"
          "1 - Give an assignment to a student\n"
          "2 - Give an assignment to a group of students\n"
          "3 - List all ungraded assignments")


def print_options4():
    print("\n"
          "GRADE ASSIGNMENT:\n"
          "1 - Grade an assignment of a student\n"
          "2 - List all graded assignments\n")


def print_options5():
    print("\n"
          "SHOW STATISTICS:\n"
          "1 - Students who received a given assignment\n"
          "2 - Students who are late in handing in at least one assignment\n"
          "3 - Students with the best school situation, ordered by average grade for all assignments")


class UI:
    def __init__(self, studentSrv, assignmentSrv, gradeSrv, undoRedoSrv):
        self.__studentSrv = studentSrv
        self.__assignmentSrv = assignmentSrv
        self.__gradeSrv = gradeSrv
        self.__undoRedoSrv = undoRedoSrv

    def ui_add_student(self):
        st_id = int(input("Student ID: "))
        name = input("Student name: ")
        group = int(input("Student group: "))
        self.__studentSrv.add_student(st_id, name, group)

    def ui_remove_student(self):
        st_id = int(input("ID of the student you wish to remove: "))
        self.__gradeSrv.remove_assignments_of_student(st_id)
        self.__studentSrv.remove_student(st_id)

    def ui_update_student(self):
        st_id = int(input("ID of the student you wish to update: "))
        new_name = input("New name: ")
        new_group = int(input("New group: "))
        self.__studentSrv.update_student(st_id, new_name, new_group)

    def ui_list_students(self):
        self.__studentSrv.list_students()

    def ui_add_assignment(self):
        as_id = int(input("Assignment ID: "))
        desc = input("Assignment description: ")
        dl = input("Assignment deadline (format: dd/mm/yyyy): ")
        self.__assignmentSrv.add_assignment(as_id, desc, dl)

    def ui_remove_assignment(self):
        as_id = int(input("ID of the assignment you wish to remove: "))
        self.__gradeSrv.remove_grades_of_assignment(as_id)
        self.__assignmentSrv.remove_assignment(as_id)

    def ui_update_assignment(self):
        as_id = int(input("ID of the assignment you wish to update: "))
        new_desc = input("New description: ")
        new_dl = input("New deadline: ")
        self.__assignmentSrv.update_assignment(as_id, new_desc, new_dl)

    def ui_list_assignments(self):
        self.__assignmentSrv.list_assignments()

    def ui_give_assignment_to_student(self):
        self.__studentSrv.list_students()
        st_id = int(input("ID of the student you wish to give an assignment to: "))
        self.__assignmentSrv.list_assignments()
        self.__gradeSrv.list_ungraded_for_student(st_id)
        self.__gradeSrv.list_graded_for_student(st_id)
        as_id = int(input("ID of the assignment: "))
        grade = None
        self.__gradeSrv.give_assignment_to_student(st_id, as_id, grade)

    def ui_give_assignment_to_group(self):
        group = int(input("The group of students you wish to give an assignment to: "))
        as_id = int(input("ID of the assignment: "))
        grade = None
        self.__gradeSrv.give_assignment_to_group(group, as_id, grade)

    def ui_list_ungraded(self):
        self.__gradeSrv.list_ungraded()

    def ui_grade_assignment(self):
        self.__studentSrv.list_students()
        st_id = int(input("ID of the student you want to grade an assignment of: "))
        if self.__gradeSrv.list_ungraded_for_student(st_id):
            as_id = int(input("\nWhich of the ungraded assignments do you wish to grade? assignment id = "))
            grade = int(input("How much do you wish to grade it? grade value = "))
            self.__gradeSrv.grade_student(st_id, as_id, grade)

    def ui_list_graded(self):
        self.__gradeSrv.list_graded()

    def ui_order_for_assignment(self):
        as_id = int(input("ID of the assignment you wish to see all graded students for: "))
        self.__gradeSrv.list_ordered_for_assignment(as_id)

    def ui_list_late_students(self):
        self.__gradeSrv.list_late_students()

    def ui_order_by_average_grade(self):
        self.__gradeSrv.order_by_avg_grade()

    def ui_undo_last_action(self):
        self.__undoRedoSrv.undo_last_action()

    def ui_redo_last_action(self):
        self.__undoRedoSrv.redo_last_action()

    def run(self):
        while True:
            print_menu_options()
            cmd = input("Option: ")
            if cmd == "x":
                print("Bye!")
                return
            try:
                if cmd == "1":
                    print_options1()
                    cmd = input("Option: ")
                    if cmd == "1":
                        self.ui_add_student()
                    elif cmd == "2":
                        self.ui_remove_student()
                    elif cmd == "3":
                        self.ui_update_student()
                    elif cmd == "4":
                        self.ui_list_students()
                    else:
                        print("Invalid option!")
                elif cmd == "2":
                    print_options2()
                    cmd = input("Option: ")
                    if cmd == "1":
                        self.ui_add_assignment()
                    elif cmd == "2":
                        self.ui_remove_assignment()
                    elif cmd == "3":
                        self.ui_update_assignment()
                    elif cmd == "4":
                        self.ui_list_assignments()
                    else:
                        print("Invalid option!")
                elif cmd == "3":
                    print_options3()
                    cmd = input("Option: ")
                    if cmd == "1":
                        self.ui_give_assignment_to_student()
                    elif cmd == "2":
                        self.ui_give_assignment_to_group()
                    elif cmd == "3":
                        self.ui_list_ungraded()
                    else:
                        print("Invalid option!")
                elif cmd == "4":
                    print_options4()
                    cmd = input("Option: ")
                    if cmd == "1":
                        self.ui_grade_assignment()
                    elif cmd == "2":
                        self.ui_list_graded()
                    else:
                        print("Invalid option!")
                elif cmd == "5":
                    print_options5()
                    cmd = input("Option: ")
                    if cmd == "1":
                        self.ui_order_for_assignment()
                    elif cmd == "2":
                        self.ui_list_late_students()
                    elif cmd == "3":
                        self.ui_order_by_average_grade()
                    else:
                        print("Invalid option!")
                elif cmd == "6":
                    self.ui_undo_last_action()
                elif cmd == "7":
                    self.ui_redo_last_action()
                else:
                    print("Invalid option!")
            except ValueError:
                print("Invalid value!\n")
            except ValidatorError as ve:
                print(ve)
            except RepositoryException as re:
                print(re)


