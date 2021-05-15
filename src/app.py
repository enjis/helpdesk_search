import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
from flask import Flask
from src import views

app = Flask(__name__)


# url routes
app.add_url_rule("/", view_func=views.root, methods=["GET"])
app.add_url_rule("/add_document", view_func=views.add_document, methods=["POST"])
app.add_url_rule("/search", view_func=views.search, methods=["POST"])

app.add_url_rule("/create_user", view_func=views.create_user, methods=["POST"])
app.add_url_rule("/delete_user", view_func=views.delete_user, methods=["POST"])
app.add_url_rule("/generate_token", view_func=views.generate_token, methods=["POST"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
