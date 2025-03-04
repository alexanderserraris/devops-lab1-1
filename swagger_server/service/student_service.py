import os
import tempfile
from functools import reduce

from tinydb import TinyDB, Query

from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017")
MONGO_DB = os.environ.get("MONGO_DB", "student_db")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]


def add(student=None):
    res = db.find_one(
        {"first_name": student.first_name, "last_name": student.last_name}
    )
    if res:
        return "already exists", 409

    doc_id = db.insert(student.to_dict())
    student.student_id = doc_id
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = db.find_one({"_id": student_id})
    if not student:
        return "not found", 404
    student["student_id"] = student_id
    print(student)
    return student


def delete(student_id=None):
    student = db.find_one({"_id": student_id})
    if not student:
        return "not found", 404
    db.delete({"_id": student_id})
    return student_id
