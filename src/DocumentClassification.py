import os

from dotenv import load_dotenv
from pymongo import MongoClient

from map_reduce.create_data_collection import create_data_collection
from map_reduce.map_reduce import map_reduce
from map_reduce.naive_bayes import NaiveBayesClassifier
from map_reduce.confusion_matrix import confusion_matrix

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
conn = MongoClient(MONGODB_URI)
db = conn.email_spam_filtering  # db chính
db1 = conn.sample_email_test  # db dùng để show quá trình xử lý của naive bayes

create_data_collection(trainned=True, db=db)
map_reduce(trained=True, db=db)
# naive_bayes_classifier = NaiveBayesClassifier(show=True, db=db)
# test_docs = "This is a test email"
# test_docs2 = "money you get from me"
# naive_bayes_classifier.classifier(test_docs)
a = confusion_matrix(db=db)
print(a)
