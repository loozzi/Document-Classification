import math

from .create_data_collection import create_preprocessed_content

class Naive_bayes_classifier:
    def __init__(self, show=False, db=None, db1=None):
        self.show = show
        self.db = db
        self.db1 = db1
        self.vocabulary = self.db.TotalCounts.find_one()["V"]
        self.class_x = self.db.TotalCounts.find_one()["clX"]
        self.class_y = self.db.TotalCounts.find_one()["clY"]
        self.denominator_x = self.class_x + self.vocabulary  # Dùng cho add-one smoothing
        self.denominator_y = self.class_y + self.vocabulary  # Dùng cho add-one smoothing
        self.check_count = 0

    def caculate_probability(self, single_doc):
        probability_class_x = 0.0
        probability_class_y = 0.0
        sum_x = 0.0 # xác suất của spam
        sum_y = 0.0 # xác suất không spam
        for word in single_doc:
            # Lấy dữ liệu từ collection WordCounts
            dict_two = self.db.WordCounts.find_one({"_id": word})
            if dict_two is not None:
                word_class_x = dict_two["claX"]  # Số lần xuất hiện của từ trong classX
                word_class_y = dict_two["claY"]  # Số lần xuất hiện của từ trong classY
            else:
                word_class_x = 0.0
                word_class_y = 0.0

            # Tính toán xác suất log với add-one smoothing
            sum_x += math.log10((word_class_x + 1.0) / self.denominator_x)
            sum_y += math.log10((word_class_y + 1.0) / self.denominator_y)

        # Thêm xác suất lớp vào tổng
        x = sum_x + probability_class_x
        y = sum_y + probability_class_y

        # Dự đoán lớp dựa trên xác suất lớn hơn
        if x > y:
            return 1, 0
        return 0, 1
    def naive_bayes_classifier(self, test_docs):
        if self.show:
            print("Mapreduce already done")
            print("Naive Bayes Classifier for mini test started")
            for doc in test_docs:
                predclassX, predclassY = self.caculate_probability(create_preprocessed_content(doc))
                # Update dự đoán vào MongoDB
                if predclassX:
                    print(f"{doc} : Spam")
                else:
                    print(f"{doc} : Not Spam")
        else:
            print("Set show=True to run the classifier")

    def naive_bayes_classifier_update_test(self):
        if not self.show:
            test_docs = self.db.test.find({"processed": {"$ne": True}}).batch_size(10)
            if(len(list(test_docs)) == 0):
                print("All documents have been processed")
                return
            
            check_count = 0

            # Dự đoán tất cả các document trong test set là classX (spam) hoặc classY (không spam)
            '''Dùng context manager để quản lý con trỏ, con trỏ sẽ tự động đóng khi dùng with như này,
            tránh lỗi timeout của cursor nếu dùng toàn bộ dữ liệu mà không thông qua batch_size'''
            with test_docs as cursor:  
                for doc in cursor:
                    predclassX, predclassY = self.caculate_probability(doc['content'])
                    # Update dự đoán vào MongoDB
                    try:
                        self.db.test.update_one(
                            {"_id": doc["_id"]},  # Sử dụng _id để xác định document
                            {"$set": {"predclassX": predclassX,
                                    "predclassY": predclassY,
                                    "processed": True}},
                        )
                    except Exception as e:
                        print(f"Error updating document")

                    # Log tiến trình
                    print(f"Processed document {check_count}")
                    check_count += 1

            print("Naive Bayes Classifier update test db done")
        else:
            print("Set show=False to run the classifier")
