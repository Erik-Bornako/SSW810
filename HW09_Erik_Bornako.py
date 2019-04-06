"""
Author: Erik Bornako
Date: 6 April 2019
SSW810 HW10
"""

from collections import defaultdict
import os
import string
from prettytable import PrettyTable
import unittest

def file_reader(directory, file_name):
    try:
        fp = open(os.path.join(directory, file_name), 'r')
    except FileNotFoundError:
        raise FileNotFoundError("Can't open ", os.path.join(directory, file_name))
    except IOError:
        raise IOError("Could not read file ", os.path.join(directory, file_name))
    else:
        return fp


class Major:

    def __init__(self, major, required_courses=set(), elective_courses=set()):
        self.major = major
        self.required_courses = required_courses #set
        self.elective_courses = elective_courses #set

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

    def __init__(self, cwid, name, department, courses):
        self.cwid = cwid
        self.name = name
        self.department = department
        self.courses = courses
    
    def add_course(self, course):
        """Adds additional student where the course has been taught"""
        self.courses[course] = self.courses.get(course, 0) + 1
        return self.courses

    def summary(self, course):
        """Returns the summary data about a single instructor"""
        return (self.cwid, self.name, self.department, course, self.courses[course])

class Repository:

    def __init__(self, dir_path, majors=set(), students=set(), instructors=set(), major_pt = PrettyTable(field_names=['Dept', 'Required', 'Electives']), student_pt=PrettyTable(field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives']),  instructor_pt=PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])):
        self.dir_path = dir_path
        self.majors = majors
        self.students = students
        self.instructors = instructors
        self.major_pt = major_pt
        self.student_pt = student_pt
        self.instructor_pt = instructor_pt
        
        fp1 = file_reader(self.dir_path, 'students.txt') 
        with fp1:
            for line in fp1:
                data = line.strip().split('\t')
                self.students.add(Student(data[0], data[1], data[2], {}))

        fp2 = file_reader(self.dir_path, 'instructors.txt') 
        with fp2:
            for line in fp2:
                data = line.strip().split('\t')
                self.instructors.add(Instructor(data[0], data[1], data[2], {}))

        fp3 = file_reader(self.dir_path, 'grades.txt')
        with fp3:
            for line in fp3:
                data = line.strip().split('\t')
                
                for student in self.students:
                    if student.cwid == data[0]:
                        student.add_grade({data[1]: data[2]})
                    else:
                        continue
                
                for instructor in self.instructors:
                    if instructor.cwid == data[3]:
                        instructor.add_course(data[1])
                    else:
                        continue
        
        fp4 = file_reader(self.dir_path, 'majors.txt')
        with fp4:
            for line in fp4:
                data = line.strip().split('\t')
                if len(self.majors) == 0:
                    self.majors.add(Major(data[0]))
                for item in self.majors:
                    if item.major != data[0]:
                        continue
                    else:
                        if data[1].lower() == 'r':
                            item.add_required_course(data[2]) # adds requred course
                            break
                        if data[1].lower() == 'e':
                            item.add_elective_course(data[2]) # adds elective course
                            break
                else:
                    if data[1].lower() == 'r':
                        self.majors.add(Major(data[0],required_courses=set([data[2]]), elective_courses=set()))
                    if data[1].lower() == 'e':
                        self.majors.add(Major(data[0],elective_courses=set([data[2]]), required_courses=set()))

        for item in self.majors:
            self.major_pt.add_row(item.summary())
        
        print(major_pt)

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
        student_pt.sortby = 'CWID'
        print(student_pt)

        for instructor in self.instructors:
            for item in instructor.courses.keys():
                self.instructor_pt.add_row(instructor.summary(item))

        print(instructor_pt)

if __name__ == '__main__':
    Repository('C:\\Users\\Erik\\Desktop\\SSW810')
