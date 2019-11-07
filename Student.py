from collections import defaultdict


class Student:
    def __init__(self, cwid, name, dept):
        self.cwid = cwid
        self.name = name
        self.courses = defaultdict(str)
        self.dept = dept
