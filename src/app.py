import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template_string, request
from pymongo import MongoClient

from map_reduce.naive_bayes import NaiveBayesClassifier

load_dotenv()

app = Flask(__name__)

db = MongoClient(os.getenv("MONGODB_URI")).email_spam_filtering


@app.route("/classifier", methods=["POST"])
def classifier():
    email = request.json["email"]
    model = NaiveBayesClassifier(show=False, db=db)
    result = model.classifier(email)
    return jsonify({"result": result})


@app.route("/", methods=["GET"])
def index():
    return render_template_string(open("./index.html", "r").read())


if __name__ == "__main__":
    app.run(port=5000)
