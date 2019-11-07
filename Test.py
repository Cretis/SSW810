from Repository import Repository
from prettytable import PrettyTable
import unittest


class TestRepository(unittest.TestCase):
    def test_raise(self):
        """this function is test every fault about my class"""
        # studentserror.txt is a file that include information with format: A\tB\tC\tD
        with self.assertRaises(IndexError):
            r = Repository('studentserror.txt', 'instructors.txt', 'grades.txt', 'majors.txt')
        with self.assertRaises(FileNotFoundError):
            r = Repository('asdasd', 'instructors.txt', 'grades.txt', 'majors.txt')
        # none.txt is a file with no information
        with self.assertRaises(IndexError):
            r = Repository('students.txt', 'none.txt', 'grades.txt', 'majors.txt')
        with self.assertRaises(IndexError):
            r = Repository('students.txt', 'instructors.txt', 'grades.txt', 'none.txt')
        with self.assertRaises(IndexError):
            r = Repository('students.txt', 'instructors.txt', 'none.txt', 'majors.txt')

    def test_Repository(self):
        """this function is test my read function of my class
        after read function , I test if there is actually read information and storage in my class"""
        r = Repository('students.txt', 'instructors.txt', 'grades.txt', 'majors.txt')
        # test the student storage
        self.assertEqual(len(r.students), 10)
        self.assertEqual(int(r.students[0].cwid), 10103)
        self.assertEqual(r.students[9].name, 'Fuller, E')
        self.assertEqual(r.students[2].dept, 'SFEN')
        # test the instructors storage
        self.assertEqual(len(r.instructors), 6)
        self.assertEqual(int(r.instructors[0].cwid), 98765)
        self.assertEqual(r.instructors[1].name, 'Feynman, R')
        self.assertEqual(r.instructors[2].dept, 'SFEN')
        # test the courses storage
        self.assertEqual([key for key in r.students[2].courses], ['SSW 555', 'SSW 567'])
        self.assertEqual(int(r.instructors[0].courses['SSW 567']), 4)
        # test the majors storage
        self.assertEqual(r.majors[0].required[0], 'SSW 540')
        self.assertEqual(r.majors[1].dept, "SYEN")
        # test the student pretty table
        pt1 = r.summarystudent()
        pt2 = PrettyTable(
            field_names=['CWID', 'Name', 'Major', 'Completed course', 'Remaining Required', 'Remaining Electives'])
        pt2.add_row(
            ['10103', 'Baldwin, C', 'SFEN', ['SSW 567', 'SSW 564', 'SSW 687', 'CS 501'], ['SSW 540', 'SSW 555'], None])
        self.assertEqual(str(pt1[0]), str(pt2))
        # test the instructor pretty table
        pt1 = r.summaryinstructor()
        pt2 = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        pt2.add_row(['98765', 'Einstein, A', 'SFEN', 'SSW 540', '2'])
        self.assertEqual(str(pt1[1]), str(pt2))
        # test the major pretty table
        pt1 = r.summarymajor()
        pt2 = PrettyTable(field_names=['Dept', 'Required', 'Elective'])
        pt2.add_row(['SFEN', ['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']])
        self.assertEqual(str(pt1[0]), str(pt2))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
