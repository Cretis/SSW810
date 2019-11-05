from collections import defaultdict


class Student:
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.courses = defaultdict(str)
        self.major = major
