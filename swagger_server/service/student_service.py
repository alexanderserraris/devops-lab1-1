import os
from pymongo import MongoClient

from swagger_server.models.student import Student

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017")
MONGO_DB = os.environ.get("MONGO_DB", "student_db")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
students_collection = db["students"]


def add(student: Student) -> int:
    res = students_collection.find_one(
        {"first_name": student.first_name, "last_name": student.last_name}
    )
    if res:
        return "already exists", 409

    student.student_id = (
        students_collection.count_documents({}) + 1
        if student.student_id is None
        else student.student_id
    )
    students_collection.insert_one(student.to_dict())
    return student.student_id


def get_by_id(student_id: int = None, subject=None) -> Student:
    student = students_collection.find_one({"student_id": int(student_id)})
    if not student:
        return "not found", 404

    return Student.from_dict(student)


def delete(student_id: int = None) -> int:
    student_id = int(student_id)
    student = students_collection.find_one({"student_id": student_id})
    if not student:
        return "not found", 404
    students_collection.delete_one({"student_id": student_id})
    return student_id
