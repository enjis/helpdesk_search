import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

from typing import Dict
from flask import request
from constants import DB_URI, SECRET_KEY
from bson.objectid import ObjectId
from pymongo import MongoClient
from src.database import db_search, db_insert
from functools import wraps
import jwt
import datetime
from utils.logger import setup_logger, logger
from werkzeug.security import check_password_hash, generate_password_hash

client = MongoClient(DB_URI, retryWrites=False)
db = client["helpdesk"]
collection = db["documents"]
user_collection = db["user"]
print("Database Connected")

setup_logger("log_info", "log/info.log")
setup_logger("log_error", "log/error.log")
setup_logger("token_logs", "log/token.log")


def token_required(f):
    """Validates the JWT token
    Returns (list): info of user calling the API
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return {"message": "Token is missing!"}, 401

        try:
            data = jwt.decode(token, SECRET_KEY)
            user = user_collection.find_one({"_id": ObjectId(data["id"])})
            if not user:
                return {"message": "Invalid Token"}, 401

        except jwt.ExpiredSignatureError:
            return {"message": "Signature has expired"}, 401
        except Exception as e:
            return {"message": "Invalid Token"}, 401

        return f(user, *args, **kwargs)

    return decorated


@token_required
def add_document(user: Dict):
    """
    Add documents to the database
    supports text and pdf
    Only accessible to admin users
    """
    logger(msg=f'Inserted document by {user["username"]}', level="info", logfile="info")

    if not user["admin"]:
        return {"message": "User is not authorized for this Operation"}

    content = request.json
    if type(content) != dict:
        return {"message": "Incorrect Parameters"}, 400
    text = content["doc"]
    try:
        db_insert(text, user["username"])
        return {"message": "Document added successfully"}, 200
    except Exception as e:
        full_traceback = traceback.format_exc()
        logger(
            msg=f"u_id: {u_id} EXCEPTION OCCURED IN PYMONGO INSERT{e} {full_traceback}",
            level="error",
            logfile="error",
        )
        return {"message": "Error occured while adding document"}, 500


def search():
    """
    Returns related documents according to the query from the database
    """

    content = request.json

    if type(content) != dict:
        return {"message": "Incorrect Parameters"}, 400
    text = content["text"]

    logger(msg=f"Search request for query: {text}", level="info", logfile="info")
    top_related_searches = db_search(text)

    return {"top_related_searches": top_related_searches}, 200


def root():
    return {"message": "Help desk Search Engine API"}


@token_required
def create_user(user: Dict):
    """Endpoint to create new user
    Args:
        user: info of user calling the API
    """

    if not user["admin"]:
        return {"message": "Not permitted to perform this operation."}, 401

    data = request.json
    if type(data) != dict:
        return {"message": "Incorrect parameters"}, 400

    search_user = user_collection.find_one({"username": data["username"]})
    if search_user:
        return {"message": "User already exists"}, 409

    user_collection.insert_one(
        {
            "admin": data["admin"],
            "password": generate_password_hash(data["password"], method="sha256"),
            "username": data["username"],
        }
    )

    logger(
        msg=f'New user created by admin with username: {data["username"]}',
        level="info",
        logfile="token",
    )
    return {"message": "User created successfully."}


@token_required
def delete_user(user: Dict):
    """Endpoint to delete a user
    Args:
        user: info of user calling the API
    """

    if not user["admin"]:
        return {"message": "Not permitted to perform this operation."}, 401

    data = request.json
    if type(data) != dict:
        return {"message": "Incorrect parameters"}, 400

    search_user = user_collection.find_one({"username": data["username"]})
    if not search_user:
        return {"message": "User not found"}, 404

    if search_user["admin"]:
        return {"message": "Not permitted to perform this operation."}, 401

    user_collection.delete_one({"username": data["username"]})

    logger(
        msg=f'User deleted by admin with username: {data["username"]}',
        level="info",
        logfile="token",
    )
    return {"message": "User deleted successfully."}


def generate_token():
    """Generates JWT token for a user
    Returns: Token with expire datetime as JSON
    """
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return {"message": "Invalid login credentials"}, 401
    user = user_collection.find_one({"username": auth.username})

    if not user:
        return {"message": "User does not exist"}, 404

    if check_password_hash(user["password"], auth.password):
        expire_datetime = datetime.datetime.utcnow() + datetime.timedelta(days=45)
        token = jwt.encode({"id": str(user["_id"]), "exp": expire_datetime}, SECRET_KEY)

        user_collection.update_one(
            {"username": auth.username}, {"$set": {"token_expire": expire_datetime}}
        )

        logger(
            msg=f"New token generated for user: {auth.username}",
            level="info",
            logfile="token",
        )
        return {"token": token.decode("UTF-8"), "expire": expire_datetime}

    return {"message": "Invalid login credentials"}, 401
