import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
from pymongo import MongoClient
from faker import Faker
from constants import DB_URI
import argparse

# print(DB_URI)
client = MongoClient(DB_URI, retryWrites=False)
db = client["helpdesk"]
collection = db["documents"]

fake = Faker()


def generate_fake_data(number: int):

    data = []
    for x in range(number):
        document = {}
        document["username"] = fake.name()
        document["text"] = fake.text()

        data.append(document)
    return data


def insert_fake_data_in_db(number: int):

    data = generate_fake_data(number)
    collection.insert_many(data)
    return {"Data Successfully Ingested"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--number",
        metavar="N",
        type=int,
        help="Number of documents to be inserted in db",
    )

    args = parser.parse_args()
    insert_fake_data_in_db(args.number)
