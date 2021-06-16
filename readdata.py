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

def main():
    studentEntitiesByID = mapStudentEntities("students.csv")
    coursesById = mapCoursesEntities("courses.csv", "tests.csv")
    assignMarksToStudents("marks.csv", studentEntitiesByID)
    # better to index courses by the set of tests (use frozen set)
    #coursesByTest = { frozenset(record.tests) : record for record in coursesById.values() }
    coursesByTest = indexByTestSet(coursesById.values())
    studentsByTest = indexByTestSet(studentEntitiesByID.values())
    print(coursesByTest)
    print(studentsByTest)
    for student in studentEntitiesByID.values():
        for course in coursesById.values():
            if any(set(course.tests.keys()).intersection(set(student.tests.keys()))):
                student.addCourse(course.id, course.name, course.teacher)

    #for _,v in studentEntitiesByID.items(): print(v)
        
    for student in studentEntitiesByID.values():
        student.calculateCourseAverage()
    try:
        for course in coursesById.values():
            course.verifyWeights()
    except Exception as e:
        print(e)
        return json.dumps({ "error" : "All course weights dont' add up to 100"})
main()

