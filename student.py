import json

class Student :
    #course: { id, name, teacher, scoreSum, courseAverage}
    def __init__(self, id, name ):
        self.id = id
        self.name = name
        self.courses =  {}
        self.tests = {}
        self.totalAverage = 0

    def addCourse(self, id, name, teacher  ):
        self.courses[id] = {"id": id, "name": name, "teacher": teacher}

    def calculateCourseAverage(self):
        # for every course, sum weight*mark and divide by len(tests)
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

    def verifyWeights(self):
        # for every course's weights, make sure add up to 100
        pass

    def __str__(self):
        return json.dumps(self.__dict__)


        """
        Course
            id    
            teacher
            name
            tests:{
                test_id:w
                test_id:w
            }
            

        }

        """





    """
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



        