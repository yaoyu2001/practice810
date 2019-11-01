# Homework 9
# Yongchang Yao 10432383
import collections
import os
from prettytable import PrettyTable


class Student:
    """Define a class as student to indicate a student"""
    PT_FIELDS = ["CWID", "Name", "Completed Courses"]

    def __init__(self, CWID, Name, Major):
        self._CWID, self._Name, self._Major = CWID, Name, Major
        self._course_rank = collections.defaultdict(str)

    def add_course(self, course, grade):
        self._course_rank[course] = grade

    def pt_row(self):
        return [self._CWID, self._Name, sorted(self._course_rank.keys())]


class Instructor:
    """Define a class as student to indicate a Instructor"""
    PT_FIELDS = ["CWID", "Name", "Dept", "Courses", "Students"]

    def __init__(self, CWID, Name, Department):
        self._CWID, self._Name, self._Department = CWID, Name, Department
        self._course_students = collections.defaultdict(int)

    def add_course(self, course):
        self._course_students[course] += 1

    def pt_row(self):
        for course, student_num in self._course_students.items():
            yield [self._CWID, self._Name, self._Department, course, student_num]


def file_reading_gen(path, fields=3, sep='\t', header=False):
    """file_reading function"""
    fp = open(path, 'r')
    with fp:
        lines = fp.readlines()
        start = 1 if header else 0
        for i in range(start, len(lines)):
            line = lines[i].strip("\n").split(sep)
            if len(line) != fields:
                raise ValueError(f"‘{os.path.basename(path)}’ has {len(line)} fields "
                                 f"on line {i if header == True else i + 1} but expected {fields}")
            else:

                yield tuple(line)


# A class to store all students instructors and grades
class Repository:
    def __init__(self, path, pttable=False):
        # Two containers to store data
        self._students = dict()
        self._instructors = dict()
        # Read data from file
        self._get_students(os.path.join(path, "students.txt"))
        self._get_instructors(os.path.join(path, "instructors.txt"))
        self._get_grade(os.path.join(path, "grades.txt"))

        if pttable:
            self._students_prettytable()
            self._instructors_prettytable()

    def _get_students(self,path):
        """Read students and populate self._students"""
        try:
            for cwid, name, major in file_reading_gen(path, 3, sep="\t",header=False):
                self._students[cwid] = Student(cwid,name,major)
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

    def _get_instructors(self, path):
        """Read instructors and populate self._instructors"""
        try:
            for cwid, name, dept in file_reading_gen(path, 3, sep="\t", header=False):
                self._instructors[cwid] = Instructor(cwid, name, dept)
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

    def _get_grade(self, path):
        try:
            for student_cwid, course, grade, instructor_cwid in file_reading_gen(path,4,sep='\t',header=False):

                try:
                    self._students[student_cwid].add_course(course, grade)
                except KeyError:
                    print(f"Found grade for unknow student {student_cwid}")

                try:
                    self._instructors[instructor_cwid].add_course(course)
                except KeyError:
                    print(f"Found grade for unknow student {instructor_cwid}")

        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

    def _students_prettytable(self):
        """Print student table"""
        pt = PrettyTable(field_names=Student.PT_FIELDS)

        for student in self._students.values():
            pt.add_row(student.pt_row())

        print("Student summary")
        print(pt)

    def _instructors_prettytable(self):
        """Print instructors table"""
        pt = PrettyTable(field_names=Instructor.PT_FIELDS)
        for instructor in self._instructors.values():
            for row in instructor.pt_row():
                pt.add_row(row)

        print("Instructor summary")
        print(pt)


def main():
    """Get paths"""
    directory = "G:\Interview\Data"

    stevens = Repository(directory, pttable=True)


if __name__ == '__main__':

    main()
