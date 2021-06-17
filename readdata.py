import os
import sys
import csv
import json
from student import Student,  Course

def mapStudentEntities(fileName):
    with open(fileName) as csvFile:
        return { int(row['id']) : Student(**row) for row in csv.DictReader(csvFile)}

def mapCoursesEntities(coursesFile, testsFile):
    coursesById = None
    with open(coursesFile) as csvFile:
        coursesById = { int(row['id']) : Course(**row) for row in csv.DictReader(csvFile)}

    assert(coursesById)
    with open(testsFile) as csvFile:
        for row in csv.DictReader(csvFile):
            course_id = int(row["course_id"])
            coursesById[course_id].addTests(row['id'], row['weight'])
    return coursesById

def assignMarksToStudents(marksFile, studentsEntities):
    with open(marksFile) as csvFile:
        for row in csv.DictReader(csvFile):
           studentsEntities[int(row["student_id"])].addTest(row["test_id"], row["mark"]) 

def indexByTestSet(data):
    return { frozenset(record.tests) : record for record in data }


def outputToJson(data, file):
    pass
    # with open(file,'w') as jsonfile:
    #     json.dumps( str(s) for s in data, jsonfile)


def matchCourseToStudent(studentsByTests, coursesByTests):
    for student_tests, student in studentsByTests.items():
        for course_tests, course in coursesByTests.items():
            print("for student id and course id: ",student.id, course.id)
            if not student_tests.isdisjoint(course_tests):
                print("Got a match for the above")
                student.addCourse(course)       

def verifyEachCourseWeights(coursesById):
    for course in coursesById.values():
        if not course.verifyWeights():
            raise ValueError("Invalid course weights")

def calculateEachStudentAverages(studentsById):
    for student in studentsById:
        student.calculateCourseAverage()

def getJsonForEachStudent(studentsById):
        data = { str(s) for s in studentsById.values() }
        return data

def main():
    try:
        coursesById = mapCoursesEntities("courses.csv", "tests.csv")
        verifyEachCourseWeights(coursesById)
        studentsById = mapStudentEntities("students.csv")
        assignMarksToStudents("marks.csv", studentsById)
        coursesIndexedByTests = indexByTestSet(coursesById.values())
        studentsIndexedByTests = indexByTestSet(studentsById.values())
        matchCourseToStudent(studentsIndexedByTests,coursesIndexedByTests)
        calculateEachStudentAverages(studentsById.values())
        # data = getJsonForEachStudent(studentsById)
        for s, val in studentsById.items():
            print(s)
            print(val)

    except ValueError as err:
        print(err.with_traceback)
        print(err)
        data = { "error": err.message}
    except Exception as err:
        print(err.with_traceback)
        print(err)
        print("Something else happened")
    finally: 
        #outputToJson(data,"output.json")
        print("Fin")

    
    
main()

