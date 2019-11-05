from prettytable import PrettyTable
from Instructor import Instructor
from Student import Student
import os


class Repository:
    def __init__(self, studentpath, instructorpath, gradepath):
        """when a object repository is created, creat 2 list to storage object student and object instructor"""
        self.students = list()
        self.instructors = list()
        self.readstudent(studentpath)
        self.readinstructor(instructorpath)
        self.readgrade(gradepath)
        print(self.summarystudent())
        print(self.summaryinstructor())

    def insertstudent(self, s):
        """this function is add object student in students list"""
        self.students.append(s)

    def insertinstructor(self, i):
        """this function is add object instructor in instructors list"""
        self.instructors.append(i)

    def summarystudent(self):
        """this function is return a pretty table about student information"""
        pt = PrettyTable(field_names=['CWID', 'Name', 'courses'])
        for student in self.students:
            pt.add_row([student.cwid, student.name, [key for key in student.courses.keys()]])
        return pt

    def summaryinstructor(self):
        """this function is return a pretty table about instructor information"""
        pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for instructor in self.instructors:
            for key in instructor.courses.keys():
                pt.add_row([instructor.cwid, instructor.name, instructor.dept, key, instructor.courses[key]])
        return pt

    def readstudent(self, path):
        """this function is read student information and storage in in to student list"""
        file_name = path
        try:
            fp = open(file_name, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f'can not find file {file_name}')
        else:
            if os.path.getsize(file_name) == 0:
                raise IndexError(f'there is no context in file{file_name}')
            with fp:
                for line in fp:
                    line = line.strip()
                    line = line.split('\t')
                    if len(line) != 3:
                        raise IndexError(f'the format of txt file {file_name} is wrong, please check it')
                    a = Student(line[0], line[1], line[2])
                    self.insertstudent(a)

    def readinstructor(self, path):
        """this function is read instructor information and storage it in to instructors list"""
        file_name = path
        try:
            fp = open(file_name, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f'can not find file {file_name}')
        else:
            if os.path.getsize(file_name) == 0:
                raise IndexError(f'there is no context in file{file_name}')
            with fp:
                for line in fp:
                    line = line.strip()
                    line = line.split('\t')
                    if len(line) != 3:
                        raise IndexError(f'the format of txt file {file_name} is wrong, please check it')
                    b = Instructor(line[0], line[1], line[2])
                    self.insertinstructor(b)

    def readgrade(self, path):
        """this function is read grade information and storage it in to student list and instructors list
        according to the cwid"""
        file_name = path
        try:
            fp = open(file_name, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f'can not find file {file_name}')
        else:
            if os.path.getsize(file_name) == 0:
                raise IndexError(f'there is no context in file{file_name}')
            with fp:
                for line in fp:
                    line = line.strip()
                    line = line.split('\t')
                    if len(line) != 4:
                        raise IndexError(f'the format of txt file {file_name} is wrong, please check it')
                    for student in self.students:
                        if int(student.cwid) == int(line[0]):
                            student.courses[line[1]] = line[2]
                            break
                    else:
                        raise KeyError(f'can not find student with cwid {line[0]}')
                    for instructor in self.instructors:
                        if int(instructor.cwid) == int(line[3]):
                            instructor.courses[line[1]] += 1
                            break
                    else:
                        raise KeyError(f'cannot find Instructor with cwid{line[3]}')


if __name__ == '__main__':
    r = Repository('students.txt', 'instructors.txt', 'grades.txt')