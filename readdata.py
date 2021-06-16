import os
import sys
import csv
from student import Student, TestScore, Course
import json

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

def splitMarks(marksFile, studentsEntities):
    with open(marksFile) as csvFile:
        for row in csv.DictReader(csvFile):
           studentsEntities[int(row["student_id"])].addTest(row["test_id"], row["mark"]) 

def main():
    studentEntitiesByID = mapStudentEntities("students.csv")
    coursesById = mapCoursesEntities("courses.csv", "tests.csv")
    # populate students with courses
    splitMarks("marks.csv", studentEntitiesByID)
    for _, student in studentEntitiesByID.items():
        for _, course in coursesById.items():
            overlap = course.tests.keys().intersection(student.tests.keys())




        




main()




