import os
import sys
import csv
import json
from typing import Iterable
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


def outputToJson(students, file):
    with open(file,'w') as jsonfile:
        json.dumps( str(s) for s in students, jsonfile)
def main():
    coursesById = mapCoursesEntities("courses.csv", "tests.csv")
    try:
        for course in coursesById.values():
            course.verifyWeights()
    except Exception as e:
        print(e)
        return json.dumps({ "error" : "All course weights dont' add up to 100"})

    studentEntitiesByID = mapStudentEntities("students.csv")
    assignMarksToStudents("marks.csv", studentEntitiesByID)
    coursesByTest = indexByTestSet(coursesById.values())
    studentsByTest = indexByTestSet(studentEntitiesByID.values())
    for student_tests, student in studentsByTest.items():
        for course_tests, course in coursesByTest.items():
            if not student_tests.isdisjoint(course_tests):
                student.addCourse(course)

    #for _,v in studentEntitiesByID.items(): print(v)
        
    for student in studentEntitiesByID.values():
        student.calculateCourseAverage()

    outputToJson(studentEntitiesByID, outputFile)
    
main()

