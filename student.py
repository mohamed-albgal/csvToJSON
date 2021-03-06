import json

class Student :
    def __init__(self, id, name ):
        self.id = id
        self.name = name
        self.courses =  {}
        self.tests = {}
        self.totalAverage = 0

    def addCourse(self, course ):
        self.courses[course.id] = { "course_id": course.id,"name":course.name, "teacher":course.teacher, "tests":course.tests }

    def calculateCourseAverage(self):
        # for every course, sum weight*mark and divide by len(tests)
        """
        course : id, name, teacher, tests: { 1:35, 2:10, 5:23}
        student: id, name, tests: {1:99, 2:88}
        stests[id] * ctests[id]
        """
        pass
    def addTest(self, test_id, mark):
        self.tests[test_id] = mark 

    def __str__(self):
        return json.dumps(self.__dict__)

class Course():
    def __init__(self, id, name, teacher) -> None:
        self.id = id
        self.name = name
        self.teacher = teacher
        self.tests = {} 
    
    def addTests(self, id, weight):
        self.tests[id] = weight
    
    def indexByTests(self):
        return { frozenset(self.tests) : self}

    def verifyWeights(self):
        return sum(int(x) for x in self.tests.values()) == 100

    def __str__(self):
        return json.dumps(self.__dict__)




    """
    Course Object:
    Course.id name teacher tests
    tests = {
        id, weight
    }
    output shape of single student object
    {
        id
        name
        totalAverage
        courses:[
            {
                id
                name
                teacher
                courseAverage (all test*weight / numtests)
                tests: {id:{}, id:{}}
            }
        ]
    }
    """



"""
marks:
    test_id, student_id, test_score


test:
    test_id, course_id, test_weight

courses:
    course_id, course_name, teacher_name

students:
    id, name

"""



        