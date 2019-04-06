"""
Author: Erik Bornako
Date: 30 March 2019
SSW810 HW09
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

class Student:

    def __init__(self, cwid, name, major, grades):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.grades = grades # grades are expected to be a dictionary of key/value pairs of courses anf there letter grades
    
    def add_grade(self, grade): # grade is a key/value pair with the course and letter grade
        """Adds course and grade into the all completed courses and grades"""
        return self.grades.update(grade)
    
    def summary(self):
        """Returns the summary data about a single student"""
        return (self.cwid, self.name, sorted(list(self.grades.keys())))


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

    def __init__(self, dir_path, students=set(), instructors=set(), student_pt=PrettyTable(field_names=['CWID', 'Name', 'Completed Courses']),  instructor_pt=PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])):
        self.dir_path = dir_path
        self.students = students
        self.instructors = instructors
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

        for student in self.students:
            self.student_pt.add_row(student.summary())

        print(student_pt)

        for instructor in self.instructors:
            for item in instructor.courses.keys():
                self.instructor_pt.add_row(instructor.summary(item))

        print(instructor_pt)

def main():
    Repository('C:\\Users\\Erik\\Desktop\\SSW810')

# main()
