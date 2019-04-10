"""
Author: Erik Bornako
Date: 10 April 2019
SSW810 HW10
"""

from collections import defaultdict
import os
import string
from prettytable import PrettyTable
import unittest
import sqlite3

def file_reader(directory, file_name, num_of_fields, sep='\t', header=False):
    try:
        fp = open(os.path.join(directory, file_name), 'r')
    except FileNotFoundError:
        raise FileNotFoundError("Can't open ", os.path.join(directory, file_name))
    except IOError:
        raise IOError("Could not read file ", os.path.join(directory, file_name))
    else:
        with fp:
            path = os.path.join(directory, file_name)
            line_number = 1
            for line in fp:
                if header == True:
                    header = False
                    continue
                else:
                    columns = tuple(line.strip().split(sep))
                    if len(columns) != num_of_fields:
                        raise ValueError(path + " has " + str(len(columns)) + " fields on line " + str(line_number) + " but expected " + str(num_of_fields))
                    else:
                        yield columns
                        line_number += 1


class Major:

    def __init__(self, major):
        self.major = major
        self.required_courses = set() #set
        self.elective_courses = set() #set

    def add_required_course(self, courses):
        return self.required_courses.add(courses)
    
    def add_elective_course(self, courses):
        return self.elective_courses.add(courses)

    def summary(self):
        return (self.major, sorted(self.required_courses), sorted(self.elective_courses))

class Student:

    def __init__(self, cwid, name, major, grades, remaining_courses=set(), remaining_electives=set()):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.grades = grades # grades are expected to be a dictionary of key/value pairs of courses anf there letter grades
        self.remaining_courses = remaining_courses
        self.remaining_electives = remaining_electives
        
    def add_grade(self, grade): # grade is a key/value pair with the course and letter grade
        """Adds course and grade into the all completed courses and grades"""
        return self.grades.update(grade)
    
    def add_remaining_courses(self, courses):
        """Assigns remaining required courses to student"""
        self.remaining_courses = courses
        return self.remaining_courses

    def add_elective_courses(self, courses):
        """Assigns remaining elective courses to student"""
        self.remaining_electives = courses
        return self.remaining_electives
    
    def summary(self):
        """Returns the summary data about a single student"""
        return (self.cwid, self.name, self.major, sorted(list(self.grades.keys())), sorted(self.remaining_courses), self.remaining_electives)


class Instructor:

    def __init__(self, cwid, name, department):
        self.cwid = cwid
        self.name = name
        self.department = department
        self.courses = defaultdict(int)
    
    def add_course(self, course):
        """Adds additional student where the course has been taught"""
        self.courses[course] += 1
        return self.courses

    def summary(self, course):
        """Returns the summary data about a single instructor"""
        return (self.cwid, self.name, self.department, course, self.courses[course])

class Repository:

    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.majors = set()
        self.students = set()
        self.instructors = set()
        self.major_pt = PrettyTable(field_names=['Dept', 'Required', 'Electives'])
        self.student_pt = PrettyTable(field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
        self.instructor_pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        
        fp1 = file_reader(self.dir_path, 'students.txt', 3) 
        for line in fp1:
            self.students.add(Student(line[0], line[1], line[2], {}))

        fp2 = file_reader(self.dir_path, 'instructors.txt', 3) 
        for line in fp2:
            self.instructors.add(Instructor(line[0], line[1], line[2]))

        fp3 = file_reader(self.dir_path, 'grades.txt', 4)
        for line in fp3:

            for student in self.students:
                if student.cwid == line[0]:
                    student.add_grade({line[1]: line[2]})
                else:
                    continue
            
            for instructor in self.instructors:
                if instructor.cwid == line[3]:
                    instructor.add_course(line[1])
                else:
                    continue
        
        fp4 = file_reader(self.dir_path, 'majors.txt', 3)
        for line in fp4:
            if len(self.majors) == 0:
                self.majors.add(Major(line[0]))
            for item in self.majors:
                if item.major != line[0]:
                    continue
                else:
                    if line[1].lower() == 'r':
                        item.add_required_course(line[2]) # adds requred course
                        break
                    if line[1].lower() == 'e':
                        item.add_elective_course(line[2]) # adds elective course
                        break
            else:
                if line[1].lower() == 'r':
                    new_major = Major(line[0])
                    new_major.add_required_course(line[2])
                    self.majors.add(new_major)
                if line[1].lower() == 'e':
                    new_major = Major(line[0])
                    new_major.add_elective_course(line[2])
                    self.majors.add(new_major)

        for item in self.majors:
            self.major_pt.add_row(item.summary())
        
        print(self.major_pt)

        for student in self.students:
            set_of_completed_courses = set()
            for completed_course, grade in student.grades.items():
                if grade in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:
                    set_of_completed_courses.add(completed_course)

            for major in self.majors:
                if student.major == major.major:
                    remaining_required = major.required_courses.difference(set_of_completed_courses)
                    remaining_electives = major.elective_courses.difference(set_of_completed_courses)
                    if remaining_electives != major.elective_courses:
                        remaining_electives = None
                    student.add_remaining_courses(remaining_required)
                    student.add_elective_courses(remaining_electives)
               
            self.student_pt.add_row(student.summary())
        self.student_pt.sortby = 'CWID'
        print(self.student_pt)

        for instructor in self.instructors:
            for item in instructor.courses.keys():
                self.instructor_pt.add_row(instructor.summary(item))

        print(self.instructor_pt)

DB_file = r'C:\Users\Erik\Desktop\SSW810\SSW810HW11.db' # file path to datebase file
db = sqlite3.connect(DB_file)

instructor_pt_with_sql = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
for row in db.execute("select Instructor_CWID, Name, Dept, Course, count(Course) As Students from HW11_instructors join HW11_grades on CWID = Instructor_CWID group by Course order by Name"):
    instructor_pt_with_sql.add_row(row)

print(instructor_pt_with_sql)

if __name__ == '__main__':
    Repository(r'C:\Users\Erik\Desktop\SSW810')

