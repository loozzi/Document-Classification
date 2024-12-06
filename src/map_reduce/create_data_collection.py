import csv
import re

from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from tqdm import tqdm

def text_to_words(raw_text):
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


def create_preprocessed_content(content):
    text = []
    new_line = text_to_words(content)
    for word in new_line.strip().split():
        word = word.encode("latin2",
                           "ignore").decode("utf-8")
        text.append(word)
    return text

def create_collection(all_dataset, db):
    
    if "all_data" in db.list_collection_names():
        db.all_data.drop()
    check_count_train = 0
    pbar = tqdm(all_dataset)
    for row in pbar:
        my_dict = {}
        class_x = 0
        class_y = 0
        my_dict["content"] = create_preprocessed_content(row["text"])
        if row["spam"] == 1:
            class_x = 1
        else:
            class_y = 1
        my_dict["classX"] = class_x
        my_dict["classY"] = class_y
        db.all_data.insert_one(my_dict)
        pbar.set_description(f"insert collection train {check_count_train}/{len(all_dataset)}")
        check_count_train += 1
    print("All data collection created")

def create_train_collection(train_dataset, db):
    
    if "train" in db.list_collection_names():
        db.train.drop()
    check_count_train = 0
    pbar = tqdm(train_dataset)
    for row in pbar:
        my_dict = {}
        class_x = 0
        class_y = 0
        my_dict["content"] = create_preprocessed_content(row["text"])
        if row["spam"] == 1:
            class_x = 1
        else:
            class_y = 1
        my_dict["classX"] = class_x
        my_dict["classY"] = class_y
        db.train.insert_one(my_dict)
        pbar.set_description(f"insert collection train {check_count_train}/{len(train_dataset)}")
        check_count_train += 1
    print("Train collection created")


def create_test_collection(test_dataset, db):
    if "test" in db.list_collection_names():
        db.test.drop()
    check_count_test = 0
    for row in test_dataset:
        my_dict = {}
        class_x = 0
        class_y = 0
        my_dict["content"] = create_preprocessed_content(row["text"])
        if row["spam"] == 1:
            class_x = 1
        else:
            class_y = 1
        my_dict["classX"] = class_x
        my_dict["classY"] = class_y
        my_dict["predclassX"] = 0
        my_dict["predclassY"] = 0
        my_dict["processed"] = False
        db.test.insert_one(my_dict)
        print(f"{check_count_test} / {len(test_dataset)}")
        check_count_test += 1
    print("Test collection created")


def create_data_collection(trainned=False, db=None):
    if trainned:
        print("Data collection already created")
        return
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
    create_collection(dataset, db)
    create_train_collection(train_dataset, db)
    create_test_collection(test_dataset, db)
