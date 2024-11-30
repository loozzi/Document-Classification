import csv
import math
import os
import re

from bson.code import Code
from dotenv import load_dotenv
from nltk.corpus import stopwords
from pymongo import MongoClient
from sklearn.model_selection import train_test_split

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
conn = MongoClient(MONGODB_URI)
db = conn.email_spam_filtering
# total number of documents in train/test set
n = 60


def create_content(content):
    text = []
    for word in content.strip().split():
        word = word.encode("latin2", "ignore").decode("utf-8")
        text.append(word)
    return text


def create_preprocessed_content(content):
    """
    :param filename:
    :return: preprocessed text (string)
    """
    text = []

    new_line = text_to_words(content)
    for word in new_line.strip().split():
        word = word.encode("latin2", "ignore").decode("utf-8")
        text.append(word)
    return text


def text_to_words(raw_text):
    """
    :param raw text:
    :return: string of words with removed stop words
    """
    # Remove non-letters
    letters_only = re.sub("[^a-zA-Z]", " ", raw_text)
    # Convert to lower case, split into individual words
    words = letters_only.lower().split()
    stops = set(stopwords.words("english"))
    # Remove stop words
    meaningful_words = [w for w in words if w not in stops]
    # Join the words back into one string separated by space,
    # and return the result.
    return " ".join(meaningful_words)


def create_train_collection(train_dataset):
    if "train" in db.list_collection_names():
        db.train.drop()
    for row in train_dataset:
        my_dict = {}
        class_x = 0
        class_y = 0
        # my_dict["content"] = create_content(row['text'])
        my_dict["content"] = create_preprocessed_content(row["text"])
        if row["spam"] == 1:
            class_x = 1
        else:
            class_y = 1
        my_dict["classX"] = class_x
        my_dict["classY"] = class_y
        db.train.insert_one(my_dict)

    print("Train collection created")


def create_test_collection(test_dataset):
    if "test" in db.list_collection_names():
        db.test.drop()
    for row in test_dataset:
        my_dict = {}
        class_x = 0
        class_y = 0
        # my_dict["content"] = create_content(row['text'])
        my_dict["content"] = create_preprocessed_content(row["text"])
        if row["spam"] == 1:
            class_x = 1
        else:
            class_y = 1
        my_dict["classX"] = class_x
        my_dict["classY"] = class_y
        my_dict["predclassX"] = 0
        my_dict["predclassY"] = 0
        db.test.insert_one(my_dict)

    print("Test collection created")


def create_data_collection():
    dataset = []
    with open("../data/emails.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        headers = next(reader)

        for row in reader:
            email = {}
            email[headers[0]] = row[0]
            email[headers[1]] = int(row[1])
            dataset.append(email)
    train_dataset, test_dataset = train_test_split(
        dataset, test_size=0.2, random_state=42, shuffle=True
    )

    create_train_collection(train_dataset)
    create_test_collection(test_dataset)


def map_reduce():
    if "TotalCounts" in db.list_collection_names():
        db.TotalCounts.drop()
    if "WordCounts" in db.list_collection_names():
        db.WordCounts.drop()

    # mapper = Code(open("map_reduce/map_type_one.js", "r").read())
    # reducer = Code(open("map_reduce/reduce_type_one.js", "r").read())
    # db.train.map_reduce(mapper, reducer, "TotalCounts")
    # print("TotalCounts collection created")

    # mapper_two = Code(open("map_reduce/map_type_two.js", "r").read())
    # reducer_two = Code(open("map_reduce/reduce_type_two.js", "r").read())
    # db.train.map_reduce(mapper_two, reducer_two, "WordCounts")
    # print("WordCounts collection created")

    pipeline_total_counts = [
        {
            "$group": {
                "_id": None,
                "totalClassX": {"$sum": "$classX"},
                "totalClassY": {"$sum": "$classY"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "clX": "$totalClassX",
                "clY": "$totalClassY",
                "V": {"$add": ["$totalClassX", "$totalClassY"]},
            }
        },
    ]

    dict_temp = list(db.train.aggregate(pipeline_total_counts))[0]
    vocabulary = dict_temp["V"]
    class_x = dict_temp["clX"]
    class_y = dict_temp["clY"]

    docs = db.train.find()

    test_docs = db.test.find()

    return vocabulary, class_x, class_y, docs, test_docs


def naive_bayes_classifier():
    vocabulary, class_x, class_y, docs, test_docs = map_reduce()
    n = 60.0
    n_class_x = 30.0
    n_class_y = 30.0
    denominator_x = class_x + vocabulary
    denominator_y = class_y + vocabulary
    probability_class_x = math.log10(n_class_x / n)
    probability_class_y = math.log10(n_class_y / n)
    for doc in test_docs:
        sum_x = 0.0
        sum_y = 0.0
        for word in doc["content"]:
            dict_two = db.WordCounts.find_one({"_id": word})
            if dict_two is not None:
                word_class_x = dict_two["value"]["classX"]
                word_class_y = dict_two["value"]["classY"]
            else:
                word_class_x = 0.0
                word_class_y = 0.0
            sum_x += math.log10((word_class_x + 1.0) / denominator_x)
            sum_y += math.log10((word_class_y + 1.0) / denominator_y)
        x = sum_x + probability_class_x
        y = sum_y + probability_class_y
        if x > y:
            db.test.update_one(doc, {"$set": {"predClassX": 1, "predClassY": 0}})
        else:
            db.test.find_one_and_update(
                doc, {"$set": {"predClassX": 0, "predClassY": 1}}
            )


def confusion_matrix():
    naive_bayes_classifier()
    mapper = Code(open("map_reduce/map_type_three.js", "r").read())
    reducer = Code(open("map_reduce/reduce_type_three.js", "r").read())
    db.test.map_reduce(mapper, reducer, "Results")

    calculated_confusion_matrix = db.Results.find_one()["value"]

    print(calculated_confusion_matrix)

    return calculated_confusion_matrix


# create_test_collection()
# create_train_collection()
create_data_collection()
a = confusion_matrix()

print(a)
