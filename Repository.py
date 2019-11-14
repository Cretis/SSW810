from prettytable import PrettyTable
from Instructor import Instructor
from Student import Student
from Major import Major
import sqlite3
import os


class Repository:
    def __init__(self, studentpath, instructorpath, gradepath, majorpath):
        """when a object repository is created, creat 2 list to storage object student and object instructor"""
        self.students = list()
        self.instructors = list()
        self.majors = list()
        try:
            self.readstudent(studentpath, True)
        except IndexError as e:
            print(e)
        try:
            self.readinstructor(instructorpath, True)
        except IndexError as e:
            print(e)

        try:
            self.readgrade(gradepath, True)
        except IndexError as e:
            print(e)
        except KeyError as e2:
            print(e2)
        try:
            self.readmajor(majorpath, True)
        except IndexError as e:
            print(e)
        except ValueError as e2:
            print(e2)
        print(self.summarystudent())
        print(self.summaryinstructor())
        print(self.summarymajor())

    def insertstudent(self, s):
        """this function is add object student in students list"""
        self.students.append(s)

    def insertinstructor(self, i):
        """this function is add object instructor in instructors list"""
        self.instructors.append(i)

    def insertmajor(self, m):
        self.majors.append(m)

    def summarystudent(self):
        """this function is return a pretty table about student information"""
        pt = PrettyTable(
            field_names=['CWID', 'Name', 'Major', 'Completed course', 'Remaining Required', 'Remaining Electives'])

        for student in self.students:
            # record remaining required
            requirecourse = list()
            # record remaining elective
            electivecourses = list()
            for major in self.majors:
                # match the dept to make sure every courses is needed for this student.
                if student.dept == major.dept:
                    # check the required courses. If course is not complete, add it into requirecourse list.
                    for item in major.required:
                        if item not in student.courses.keys():
                            requirecourse.append(item)
                    else:
                        if not requirecourse:
                            requirecourse = None
                    # check the elective courses.
                    # If there is at least one elective course completed,
                    # the student do not need to choos another elective course,electivecourses equal to none
                    # IF not, add all of elective courses into electivecourses list.
                    for item in major.elective:
                        if item in student.courses.keys():
                            electivecourses = None
                            break
                    else:
                        electivecourses = major.elective
            pt.add_row([student.cwid, student.name, student.dept, [key for key in student.courses], requirecourse,
                        electivecourses])
        return pt

    def summaryinstructor(self):
        """this function is return a pretty table about instructor information"""
        pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for instructor in self.instructors:
            for key in instructor.courses.keys():
                pt.add_row([instructor.cwid, instructor.name, instructor.dept, key, instructor.courses[key]])
        return pt

    def summarymajor(self):
        """this function is return a pretty table about major information"""
        pt = PrettyTable(field_names=['Dept', 'Required', 'Elective'])
        for major in self.majors:
            pt.add_row([major.dept, major.required, major.elective])
        return pt

    def readstudent(self, path, header=False):
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
                    # if header is True, pass the first line
                    if header is True:
                        header = False
                        continue
                    line = line.strip()
                    line = line.split('\t')
                    if len(line) != 3:
                        raise IndexError(f'the format of txt file {file_name} is wrong, please check it')
                    a = Student(line[0], line[1], line[2])
                    self.insertstudent(a)

    def readinstructor(self, path, header=False):
        """this function is read instructor information and storage it in to instructors list"""
        file_name = path
        try:
            fp = open(file_name, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f'can not find file {file_name}')
        else:
            # make sure it is not a none file
            if os.path.getsize(file_name) == 0:
                raise IndexError(f'there is no context in file{file_name}')
            with fp:
                for line in fp:
                    # if header is True, pass the first line
                    if header is True:
                        header = False
                        continue
                    line = line.strip()
                    line = line.split('\t')
                    if len(line) != 3:
                        raise IndexError(f'the format of txt file {file_name} is wrong, please check it')
                    b = Instructor(line[0], line[1], line[2])
                    self.insertinstructor(b)

    def readgrade(self, path, header=False):
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
                    # if header is True, pass the first line
                    if header is True:
                        header = False
                        continue
                    line = line.strip()
                    line = line.split('\t')
                    if len(line) != 4:
                        raise IndexError(f'the format of txt file {file_name} is wrong, please check it')
                    # check the grade, if student get a secore lower than C, he need repeat course
                    if line[2] in ['A', 'B', 'C', 'A-', 'B+', 'B-', 'C+']:
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
                            raise KeyError(f'cannot find Instructor with cwid {line[3]}')

    def readmajor(self, path, header=False):
        """this function is read file about information of major and storage it in to list majors"""
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
                    if header is True:
                        header = False
                        continue
                    line = line.strip()
                    line = line.split('\t')
                    if len(line) != 3:
                        raise IndexError(f'the format of txt file {file_name} is wrong, please check it')
                    # find the which major have same dept with dept in this line, storage course in this object.
                    # if there not have same dept, create new major object to storage course with this dept
                    for major in self.majors:
                        if major.dept == line[0]:
                            if line[1] == 'R':
                                major.required.append(line[2])
                                break
                            elif line[1] == 'E':
                                major.elective.append(line[2])
                                break
                            else:
                                raise ValueError(
                                    f'the context of elective/Required is wrong, please check file{file_name}')
                    else:
                        # create new object and add the courses in this object
                        c = Major(line[0])
                        if line[1] == "R":
                            c.required.append(line[2])
                        elif line[2] == 'E':
                            c.elective.append(line[2])
                        else:
                            raise ValueError(
                                f'the context of elective/Required is wrong, please check file{file_name}')
                        self.insertmajor(c)

    def instructor_table_db(self, db_path):
        db = sqlite3.connect(db_path)
        pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for row in db.execute(
                "select * from instructor_summary"):
            pt.add_row(row)
        db.close()
        return pt


if __name__ == '__main__':
    r = Repository('students.txt', 'instructors.txt', 'grades.txt', 'majors.txt')
    print(r.instructor_table_db('/Users/fst/database/SSW810'))
