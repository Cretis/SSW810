from collections import defaultdict
class Instructor:
    def __init__(self,cwid,name,dept):
        self.cwid = cwid
        self.dept = dept
        self.name = name
        self.courses = defaultdict(int)
