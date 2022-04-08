

class Student:
    def __init__(self, st_id, name, group):
        self.__st_id = st_id
        self.__name = name
        self.__group = group

    def get_st_id(self):
        return self.__st_id

    def get_name(self):
        return self.__name

    def set_name(self, value):
        self.__name = value

    def get_group(self):
        return self.__group

    def set_group(self, value):
        self.__group = value

    def __str__(self):
        return "Student: {0}, Name: {1}, Group: {2}".format(self.__st_id, self.__name, self.__group)

    def __eq__(self, other):
        return self.__st_id == other.__st_id


class Assignment:
    def __init__(self, as_id, desc, dl):
        self.__as_id = as_id
        self.__desc = desc
        self.__dl = dl
    
    def get_as_id(self):
        return self.__as_id

    def get_desc(self):
        return self.__desc
    
    def set_desc(self, value):
        self.__desc = value

    def get_dl(self):
        return self.__dl

    def set_dl(self, value):
        self.__dl = value

    def __str__(self):
        return "Assignment: {0}, Description: {1}, Deadline: {2}".format(self.__as_id, self.__desc, self.__dl)

    def __eq__(self, other):
        return self.__as_id == other.__as_id


class Grade:
    def __init__(self, st_id, as_id, grade):
        self.__st_id = st_id
        self.__as_id = as_id
        self.__grade = grade

    def get_as_id(self):
        return self.__as_id

    def get_st_id(self):
        return self.__st_id

    def get_grade(self):
        return self.__grade

    def set_grade(self, value):
        self.__grade = value

    def __str__(self):
        return "(Student: {0}, Assignment: {1}, Grade: {2})".format(self.__st_id, self.__as_id, self.__grade)

    def __eq__(self, other):
        return (self.__st_id == other.__st_id) and (self.__as_id == other.__as_id)


class UndoRedoAction:
    def __init__(self, action, obj):
        self.__action = action
        self.__obj = obj

    def get_action(self):
        return self.__action

    def get_object(self):
        return self.__obj
