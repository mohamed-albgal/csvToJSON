import csv
import json

class StudentRecord:

    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.courses = {}
        self.tests = {}

    def addTest(self,tid,cid,score,weight):
        test = self.tests.get(tid, {tid:{}})
        test.update(test_id=tid, score=score, weight=weight)
        self[tid] = test
    
    def addCourse(self,cid, name,teacher):
        course = self.courses.get(cid,{})
        course.update(name=name, teacher=teacher)
        self.courses[cid] = course

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)

def readCsvOneToMany(filename):
    records = dict()
    # records: tid: {sid:{1:12}} 1: students: {12:83}
    # tid: { sid: value} -> 1: {12: 83}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            #assuming field names are tid, sid mark
            tid,sid,mark = row.values()
            mapping = records.get(tid, {sid:{} })
            mapping.update({sid:{"score":mark}})
            records[tid] = mapping
    return records

def readCsvOneToOne(filename, fieldNames=None):
    records = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        fields = fieldNames if fieldNames else reader.fieldnames
        for row in reader:
            record = {row['id'] : {}}
            for field in fields:
                if field == 'id': continue
                if field not in row:
                    raise ValueError(f"Expected key: {field} not found in file")
                record[row['id']][field] = row[field] 
            records.update(record)
    return records
                
def getTestResults(testsFile, marksFile):
    testResultsByTID = readCsvOneToMany(marksFile)
    with open(testsFile) as f:
        reader = csv.DictReader(f)
        for row in reader:
            #assert the field names
            tid, cid, wt = row.values()
            if tid in testResultsByTID:
                testResultsByTID.get(tid).update(courseID=cid, weight=wt)
    return testResultsByTID

def createStudentInstances(students):
    studentObjects = {}
    for id,info in students.items():
        studentObjects[id] = (StudentRecord(id,info['name']))
    return studentObjects

def main():
    studentsByID = readCsvOneToOne("students.csv")
    testDetails = getTestResults("tests.csv", "marks.csv")
    coursesByID = readCsvOneToOne("courses.csv", {"name","teacher"})
    students = createStudentInstances(studentsByID)
    for  sid, student in students.items():
        if sid in testDetails:
            studentTestDetails = testDetails[sid]
            for key,value in studentTestDetails.items():
                if key == 'courseID':
                    cid = value
                    courseInfo = coursesByID[cid]
                    student.addCourse(cid, **courseInfo)
                    print(student)

main()

"""
    {
        id
        name
        totalAverage
        courses:[ # make course a key, and get courses
            {
                id
                name
                teacher
                tests:{
                    id, score, weight
                }
                #courseAverage (all test*weight / numtests)


            }
        ]
    }

 i have students like id:name
 
    i have a record of:

    {tid:{
        sid:{
            score:val
        }
        sid:{
            score: val
        }
        .
        .
        .
        
    }
    .
    .
    
    }

"""
