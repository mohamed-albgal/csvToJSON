import csv

class StudentRecord:

    def __init__(self,id):
        self.id = id
    def addCourseInfo():
        pass
    

def readMarksFile():
    # get the marks csv into memory
    with open("marks.csv") as f:
        reader = csv.DictReader(f)
        return { row["test_id"]: {"student_id":int(row['student_id']), "mark":int(row["mark"])} for row in reader}

def denormalizeTestsIntoMarks(marks):
    #read the lines of for every test_id in the marks file:
    #that we find here, add to that dict: course_id and weight 
    with open("tests.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tid = row["id"]
            if tid in marks:
                marks.get(tid).update({ "course_id":row["course_id"], "weight":row["weight"]})
    
def readTests(testFile):
    with open(testFile) as f:
        reader = csv.DictReader(f)
        return {int(row["id"]):{"course_id":int(row["course_id"]), "weight":int(row["weight"])} for row in reader}

def mergeCoursesIntoTests(tests, coursesFile):
    with open(coursesFile) as f:
        reader = csv.DictReader(f)
        for row in reader:
            

def main():
    #merge courses into tests to get shape:
    tests = readTests("tests.csv")
    mergeCoursesIntoTests(tests,"courses.csv")
    

main()

"""
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
            }
        ]
    }


new plan:

merge courses into tests to get shape:
    { tid, cide, naem, teacher, weight}

merge that then into marks and index by test id to get:

    {
        sid, tid, cid , name, teacher, marks, weight
    } 
    a collection of tests records

for every id in test:
    map_value = mylistofStudentInstances.get(id[sid],Student(id[sid])
    map_value.tests[id] = testlist[id]
    # now we've updated the internal test list for the student with the test info
    now add the course info





    """