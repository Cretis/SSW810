from Repository import Repository
import unittest


class TestRepository(unittest.TestCase):
    def test_raise(self):
        """this function is test every fault about my class"""
        r = Repository()
        # studentserror.txt is a file that include information with format: A\tB\tC\tD
        with self.assertRaises(IndexError):
            r.readstudent('studentserror.txt')
        with self.assertRaises(FileNotFoundError):
            r.readstudent('asdfsf')
        # none.txt is a file with no information
        with self.assertRaises(IndexError):
            r.readinstructor('none.txt')
        with self.assertRaises(IndexError):
            r.readgrade('none.txt')
        with self.assertRaises(IndexError):
            r.readstudent('none.txt')

    def test_read(self):
        """this function is test my read function of my class
        after read function , I test if there is actually read information and storage in my class"""
        r = Repository('students.txt', 'instructors.txt', 'grades.txt')

        self.assertEqual(len(r.students), 10)
        self.assertEqual(int(r.students[0].cwid), 10103)
        self.assertEqual(r.students[9].name, 'Fuller, E')
        self.assertEqual(r.students[2].major, 'SFEN')

        self.assertEqual(len(r.instructors), 6)
        self.assertEqual(int(r.instructors[0].cwid), 98765)
        self.assertEqual(r.instructors[1].name, 'Feynman, R')
        self.assertEqual(r.instructors[2].dept, 'SFEN')

        self.assertEqual([key for key in r.students[2].courses], ['SSW 555', 'SSW 567'])
        self.assertEqual(int(r.instructors[0].courses['SSW 567']), 4)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
