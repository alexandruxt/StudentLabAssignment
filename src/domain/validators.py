
class ValidatorError(Exception):
    pass


class StudentValidator:
    def validate(self, student):
        errors = ""
        if student.get_st_id() < 0:
            errors += "Invalid ID!\n"
        if student.get_name() == "":
            errors += "Invalid name!\n"
        if student.get_group() < 0:
            errors += "Invalid group!"
        if len(errors) > 0:
            raise ValidatorError(errors)


class AssignmentValidator:
    def validate(self, assignment):
        errors = ""
        if assignment.get_as_id() < 0:
            errors += "Invalid ID!\n"
        if assignment.get_desc() == "":
            errors += "Invalid description!\n"
        k = True
        deadline = assignment.get_dl().split("/")
        if len(deadline) != 3:
            k = False
        else:
            if not deadline[0].isnumeric():
                k = False
            elif not isinstance(int(deadline[0]), int):
                k = False
            elif int(deadline[0]) < 1 or int(deadline[0]) > 31:
                k = False
            if not deadline[1].isnumeric():
                k = False
            elif not isinstance(int(deadline[1]), int):
                k = False
            elif int(deadline[1]) < 1 or int(deadline[1]) > 12:
                k = False
            if not deadline[2].isnumeric():
                k = False
            elif not isinstance(int(deadline[2]), int):
                k = False
            elif int(deadline[2]) < 1000 or int(deadline[2]) > 9999:
                k = False
        if k is False:
            errors += "Invalid deadline!"
        if len(errors) > 0:
            raise ValidatorError(errors)


class GradeValidator:
    def validate(self, grade):
        errors = ""
        if grade.get_as_id() < 0:
            errors += "Invalid Assignment ID!\n"
        if grade.get_st_id() < 0:
            errors += "Invalid Student ID!\n"
        if grade.get_grade() < 0:
            errors += "Invalid grade value!"
        if len(errors) > 0:
            raise ValidatorError(errors)
