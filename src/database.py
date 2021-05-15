from typing import List
from pymongo import MongoClient
from constants import DB_URI

print(DB_URI)
client = MongoClient(DB_URI, retryWrites=False)
db = client["helpdesk"]
collection = db["documents"]


def db_insert(text: str, user: str):

    data = [{"username": user, "text": text}]
    collection.insert_many(data)
    return {"Data Successfully Ingested"}


def db_search(text: str):
    filter_query = {"$text": {"$search": text}}
    projection = {"score": {"$meta": "textScore"}, "_id": 0}

    related_documents = collection.find(filter_query, projection).sort(
        [("score", {"$meta": "textScore"})]
    )

    return list(related_documents)
