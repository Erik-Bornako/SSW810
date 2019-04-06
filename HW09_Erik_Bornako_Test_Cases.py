from HW09_Erik_Bornako import Repository
import unittest

class RepositoryTest(unittest.TestCase):
    def test_repository(self):
        stevens = Repository('C:\\Users\\Erik\\Desktop\\SSW810')
        student_lst = []
        for student in stevens.students:
            student_lst.append(student.summary())
        instructor_lst = []
        for instructor in stevens.instructors:
            for course in instructor.courses:
                instructor_lst.append(instructor.summary(course))
        self.assertEqual(sorted(student_lst), [('10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']), ('10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']), ('10172', 'Forbes, I', ['SSW 555', 'SSW 567']), ('10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687']), ('10183', 'Chapman, O', ['SSW 689']), ('11399', 'Cordova, I', ['SSW 540']), ('11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800']), ('11658', 'Kelly, P', ['SSW 540']), ('11714', 'Morton, A', ['SYS 611', 'SYS 645']), ('11788', 'Fuller, E', ['SSW 540'])])
        self.assertEqual(sorted(instructor_lst), [('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2), ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1), ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1), ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1), ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1), ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1), ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1), ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1), ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3), ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3), ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3), ('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4)])
        with self.assertRaises(FileNotFoundError):
            Repository('blahblahblah')

if __name__ == '__main__':
    unittest.main(exit=False,verbosity=2)