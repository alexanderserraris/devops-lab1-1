import os
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017")
MONGO_DB = os.environ.get("MONGO_DB", "student_db")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
students_collection = db["students"]


def add(student=None):
    res = students_collection.find_one(
        {"first_name": student.first_name, "last_name": student.last_name}
    )
    if res:
        return "already exists", 409

    doc_id = students_collection.insert_one(student.to_dict()).inserted_id
    return str(doc_id)  # we need to stringify the ObjectId for valid JSON


def get_by_id(student_id=None, subject=None):
    student = students_collection.find_one({"_id": student_id})
    if not student:
        return "not found", 404
    student["student_id"] = student_id
    print(student)
    return student


def delete(student_id=None):
    student = students_collection.find_one({"_id": student_id})
    if not student:
        return "not found", 404
    students_collection.delete_one({"_id": student_id})
    return student_id
